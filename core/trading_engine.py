from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class TradingEngine:
    def __init__(self):
        self.settings = settings
        self.executor = None  # Initialisation différée
        logger.info("Moteur de trading initialisé")

    def initialize_executor(self):
        # Initialisation différée pour éviter les dépendances circulaires
        from core.pine_executor import PineExecutor
        self.executor = PineExecutor()
        logger.info("Exécuteur de stratégie initialisé")

    def execute_strategy(self, strategy_name=None, symbol=None):
        # Vérifiez que l'exécuteur est initialisé
        if not self.executor:
            self.initialize_executor()
            
        strategy = strategy_name or self.settings.DEFAULT_STRATEGY
        symbol = symbol or self.settings.DEFAULT_SYMBOL
        
        logger.info(f"Début d'exécution de la stratégie: {strategy} sur {symbol}")
        
        try:
            result = self.executor.execute_strategy(strategy, symbol)
            logger.info(f"Résultat de la stratégie: {result}")
            return result
        except Exception as e:
            logger.error(f"Erreur d'exécution: {str(e)}", exc_info=True)
            raise
