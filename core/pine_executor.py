import os
import re
from datetime import datetime
from binance.client import Client
from config.settings import settings
import logging
import talib  # Pour les calculs techniques avancés
import numpy as np

logger = logging.getLogger(__name__)

class PineExecutor:
    def __init__(self):
        # Initialiser le client Binance
        self.client = Client(
            settings.BINANCE_API_KEY,
            settings.BINANCE_SECRET_KEY,
            testnet=settings.BINANCE_TESTNET
        )
    
    def execute_strategy(self, strategy_name, symbol):
        strategy_file = f"{strategy_name}.pine"
        strategy_path = os.path.join(settings.PINE_SCRIPT_PATH, strategy_file)
        
        if not os.path.exists(strategy_path):
            raise FileNotFoundError(f"Stratégie non trouvée: {strategy_file}")
        
        # Lire le script Pine
        with open(strategy_path, 'r') as f:
            pine_script = f.read()
        
        # Analyser le script pour déterminer le type de stratégie
        if "rsi(" in pine_script.lower():
            return self.execute_rsi_strategy(symbol, pine_script)
        elif "macd(" in pine_script.lower():
            return self.execute_macd_strategy(symbol, pine_script)
        elif "ema(" in pine_script.lower():
            return self.execute_ema_strategy(symbol, pine_script)
        else:
            raise ValueError("Type de stratégie non reconnu dans le script Pine")
    
    def execute_rsi_strategy(self, symbol, pine_script):
        """Exécute une stratégie basée sur le RSI"""
        # Extraire les paramètres du script
        params = self.parse_rsi_params(pine_script)
        
        # Récupérer les données
        data = self.get_ohlc_data(symbol, params['interval'], params['limit'])
        
        # Calculer le RSI
        closes = np.array([float(d[4]) for d in data])
        rsi_values = talib.RSI(closes, timeperiod=params['length'])
        
        # Dernière valeur RSI
        last_rsi = rsi_values[-1] if len(rsi_values) > 0 else 50
        
        # Décision de trading
        signal = "HOLD"
        if last_rsi < params['oversold']:
            signal = "BUY"
        elif last_rsi > params['overbought']:
            signal = "SELL"
        
        return {
            'strategy': 'RSI',
            'symbol': symbol,
            'rsi': last_rsi,
            'signal': signal,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def execute_macd_strategy(self, symbol, pine_script):
        """Exécute une stratégie basée sur le MACD"""
        # Extraire les paramètres du script
        params = self.parse_macd_params(pine_script)
        
        # Récupérer les données
        data = self.get_ohlc_data(symbol, params['interval'], params['limit'])
        
        # Calculer le MACD
        closes = np.array([float(d[4]) for d in data])
        macd, signal, _ = talib.MACD(
            closes, 
            fastperiod=params['fast'], 
            slowperiod=params['slow'], 
            signalperiod=params['signal_period']
        )
        
        # Décision de trading
        signal_value = "HOLD"
        if macd[-1] > signal[-1] and macd[-2] <= signal[-2]:
            signal_value = "BUY"
        elif macd[-1] < signal[-1] and macd[-2] >= signal[-2]:
            signal_value = "SELL"
        
        return {
            'strategy': 'MACD',
            'symbol': symbol,
            'macd': macd[-1],
            'signal_line': signal[-1],
            'signal': signal_value,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def parse_rsi_params(self, pine_script):
        """Extrait les paramètres RSI du script Pine"""
        # Valeurs par défaut
        params = {
            'length': 14,
            'oversold': 30,
            'overbought': 70,
            'interval': '1h',
            'limit': 100
        }
        
        # Trouver les paramètres dans le script
        try:
            params['length'] = int(self.extract_param(pine_script, 'length', 14))
            params['oversold'] = int(self.extract_param(pine_script, 'oversold', 30))
            params['overbought'] = int(self.extract_param(pine_script, 'overbought', 70))
            params['interval'] = self.extract_interval(pine_script)
        except Exception as e:
            logger.warning(f"Erreur d'analyse des paramètres RSI: {e}")
        
        return params
    
    def parse_macd_params(self, pine_script):
        """Extrait les paramètres MACD du script Pine"""
        # Valeurs par défaut
        params = {
            'fast': 12,
            'slow': 26,
            'signal_period': 9,
            'interval': '1h',
            'limit': 100
        }
        
        # Trouver les paramètres dans le script
        try:
            params['fast'] = int(self.extract_param(pine_script, 'fast', 12))
            params['slow'] = int(self.extract_param(pine_script, 'slow', 26))
            params['signal_period'] = int(self.extract_param(pine_script, 'signal', 9))
            params['interval'] = self.extract_interval(pine_script)
        except Exception as e:
            logger.warning(f"Erreur d'analyse des paramètres MACD: {e}")
        
        return params
    
    def extract_param(self, script, param_name, default):
        """Extrait un paramètre numérique du script"""
        pattern = re.compile(rf'{param_name}\s*=\s*input\((\d+)')
        match = pattern.search(script)
        return match.group(1) if match else default
    
    def extract_interval(self, script):
        """Extrait l'intervalle du script"""
        match = re.search(r'interval\s*=\s*input.timeframe\("([^"]+)"', script)
        return match.group(1) if match else '1h'
    
    def get_ohlc_data(self, symbol, interval, limit=100):
        """Récupère les données OHLC de Binance"""
        try:
            return self.client.get_klines(
                symbol=symbol,
                interval=interval,
                limit=limit
            )
        except Exception as e:
            logger.error(f"Erreur de récupération des données: {str(e)}")
            raise
