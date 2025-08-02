import os
from pathlib import Path

class Settings:
    def __init__(self):
        # Configuration de base
        self.PORT = int(os.getenv("PORT", "5000"))
        
        # Configuration des stratégies
        self.STRATEGY_TYPE = os.getenv("STRATEGY_TYPE", "pine")
        self.DEFAULT_STRATEGY = os.getenv("DEFAULT_STRATEGY", "rsi_strategy")
        self.DEFAULT_SYMBOL = os.getenv("DEFAULT_SYMBOL", "BTCUSDT")
        self.STRATEGY_SCHEDULE = os.getenv("STRATEGY_SCHEDULE", "*/15 * * * *")
        
        # Sécurité
        self.WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "change_this_secret")
        self.BINANCE_API_KEY = os.getenv("BINANCE_API_KEY", "")
        self.BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY", "")
        self.BINANCE_TESTNET = os.getenv("BINANCE_TESTNET", "true").lower() == "true"
        
        # Chemins
        self._init_paths()
    
    def _init_paths(self):
        """Initialise les chemins de manière fiable"""
        # Chemin absolu du répertoire config
        base_dir = Path(__file__).resolve().parent
        
        # Chemin vers les stratégies Pine
        self.PINE_SCRIPT_PATH = base_dir.parent / "strategies" / "pine_strategies"
        
        # Créer les répertoires si inexistants
        self.PINE_SCRIPT_PATH.mkdir(parents=True, exist_ok=True)
        
        # Validation
        self._validate_paths()
    
    def _validate_paths(self):
        """Vérifie que les chemins essentiels existent"""
        if not self.PINE_SCRIPT_PATH.exists():
            raise RuntimeError(f"PINE_SCRIPT_PATH introuvable: {self.PINE_SCRIPT_PATH}")
        
        if not any(self.PINE_SCRIPT_PATH.glob("*.pine")):
            print(f"Attention: Aucune stratégie Pine trouvée dans {self.PINE_SCRIPT_PATH}")

# Instance singleton pour l'application
settings = Settings()
