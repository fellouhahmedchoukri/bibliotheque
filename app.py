from flask import Flask, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from core.trading_engine import TradingEngine
from config.settings import settings
from webhooks.binance_webhook import handle_binance_webhook
import logging
from datetime import datetime
import time
from threading import Thread
from queue import Queue
import os

# Configurer le logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Créer une queue pour les logs
log_queue = Queue()

# Handler pour envoyer les logs à la queue
class QueueHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        log_queue.put(log_entry)

# Ajouter le handler au logger principal
root_logger = logging.getLogger()
queue_handler = QueueHandler()
root_logger.addHandler(queue_handler)

# Initialiser le moteur de trading
engine = TradingEngine()
engine.initialize_executor()

logger.info("Moteur de trading initialisé avec succès")

# Configuration du scheduler
scheduler = None
if settings.STRATEGY_SCHEDULE:
    scheduler = BackgroundScheduler(daemon=True)
    cron_parts = settings.STRATEGY_SCHEDULE.split()
    
    if len(cron_parts) == 5:
        scheduler.add_job(
            engine.execute_strategy,
            'cron',
            minute=cron_parts[0],
            hour=cron_parts[1],
            day=cron_parts[2],
            month=cron_parts[3],
            day_of_week=cron_parts[4]
        )
        scheduler.start()
        logger.info(f"Scheduler configuré avec: {settings.STRATEGY_SCHEDULE}")
    else:
        logger.error(f"Format de schedule invalide: {settings.STRATEGY_SCHEDULE}")

# Routes du tableau de bord
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/strategies')
def strategies():
    return render_template('strategies.html')

@app.route('/logs')
def logs():
    return render_template('logs.html')

# API Endpoints
@app.route('/api/dashboard')
def dashboard_data():
    return jsonify({
        "performance": {
            "labels": ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun"],
            "values": [100, 120, 90, 150, 130, 180]
        },
        "recent_executions": [
            {
                "timestamp": datetime.now().isoformat(),
                "strategy": "rsi_strategy",
                "symbol": "BTCUSDT",
                "result": "BUY",
                "success": True
            },
            {
                "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(),
                "strategy": "macd_strategy",
                "symbol": "ETHUSDT",
                "result": "HOLD",
                "success": True
            }
        ],
        "last_execution": datetime.now().isoformat(),
        "next_execution": (datetime.now() + timedelta(minutes=5)).isoformat() if scheduler else None
    })

@app.route('/api/strategies')
def list_strategies():
    from pathlib import Path
    strategies_dir = Path(settings.PINE_SCRIPT_PATH)
    
    if not strategies_dir.exists():
        return jsonify({"error": "Dossier des stratégies introuvable"}), 500
    
    strategies = []
    for file in strategies_dir.glob('*'):
        if file.is_file():
            strategies.append({
                "name": file.stem,
                "last_executed": datetime.now().isoformat(),
                "success_count": 12,
                "total_count": 15,
                "active": True
            })
    
    return jsonify(strategies)

# Flux de logs SSE
@app.route('/logs')
def stream_logs():
    def generate():
        while True:
            if not log_queue.empty():
                yield f"data: {log_queue.get()}\n\n"
            time.sleep(0.1)
    return Response(generate(), mimetype='text/event-stream')

# Route webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    return handle_binance_webhook()

# Route santé
@app.route('/health')
def health_check():
    return 'OK', 200

if __name__ == '__main__':
    port = int(settings.PORT)
    logger.info(f"Démarrage de l'application sur le port {port}")
    app.run(host='0.0.0.0', port=port)
