from flask import request, jsonify
from core.trading_engine import TradingEngine
from config.settings import Settings
import hmac
import hashlib

def verify_signature(data, signature):
    secret = Settings().WEBHOOK_SECRET.encode()
    expected = hmac.new(secret, data, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)

def handle_binance_webhook():
    data = request.get_data()
    signature = request.headers.get('X-Signature', '')
    
    if not verify_signature(data, signature):
        return jsonify({"error": "Signature invalide"}), 401
    
    payload = request.json
    strategy = payload.get('strategy')
    symbol = payload.get('symbol')
    
    engine = TradingEngine()
    result = engine.execute_strategy(strategy, symbol)
    
    return jsonify({"status": "success", "result": result})
