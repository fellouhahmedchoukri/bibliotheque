# Bibliothèque de Trading Algorithmique

[![Déployer sur Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/fellouhahmedchoukri/bibliotheque)

Ce projet est un système de trading automatisé pour Binance qui exécute des stratégies de trading codées en Pine Script. Il permet une intégration transparente avec TradingView via des webhooks sécurisés.

## Fonctionnalités Clés

- 🚀 **Exécution de stratégies Pine Script** sur Binance
- 🔒 **Validation HMAC** pour la sécurité des webhooks
- 📊 **Gestion des stratégies** via API REST
- 🤖 **Architecture modulaire** facile à étendre
- ☁️ **Déploiement 1-clic** sur Railway

## Architecture du Projet

```plaintext
bibliotheque/
├── app.py                        # Point d'entrée principal
├── core/                         # Logique métier
│   ├── trading_engine.py         # Moteur d'exécution des trades
│   └── pine_adapter.py           # Adaptateur pour stratégies Pine
├── strategies/                   # Répertoire des stratégies
│   └── pine_strategies/          # Stratégies Pine Script
├── webhooks/                     # Gestion des webhooks
│   └── binance_webhook.py        # Endpoint webhook Binance
└── config/                       # Configuration

# Bibliothèque de Stratégies de Trading Automatisées

![Dashboard Preview](https://via.placeholder.com/800x400?text=Dashboard+Preview)

Ce projet permet d'automatiser l'exécution de stratégies de trading sur Binance à l'aide de scripts Pine Script. Il offre un tableau de bord complet pour surveiller les performances et gérer les stratégies.

## Fonctionnalités principales

- 🚀 Exécution automatique de stratégies Pine Script
- 🔔 Déclenchement par webhook ou planificateur
- 📊 Tableau de bord de monitoring complet
- 🔐 Sécurité renforcée avec signature HMAC
- 📈 Visualisation des performances des stratégies
- 🔧 Gestion des stratégies en temps réel

## Architecture

```mermaid
graph TD
    A[Tableau de bord Web] --> B[API Flask]
    B --> C[Moteur de Trading]
    C --> D[Exécuteur Pine]
    D --> E[API Binance]
    F[Webhook] --> B
    G[Planificateur] --> C

Déploiement
Prérequis
Compte Binance (avec API Key)

Compte Railway

Étapes de déploiement
Cloner le dépôt:

bash
git clone https://github.com/fellouhahmedchoukri/bibliotheque.git
cd bibliotheque
Configurer les variables d'environnement:
Créez un fichier .env:

env
BINANCE_API_KEY=votre_api_key
BINANCE_SECRET_KEY=votre_api_secret
BINANCE_TESTNET=true
PORT=5000
WEBHOOK_SECRET=un_secret_complexe
STRATEGY_TYPE=pine
DEFAULT_STRATEGY=rsi_strategy
DEFAULT_SYMBOL=BTCUSDT
STRATEGY_SCHEDULE="*/5 * * * *"
Déployer sur Railway:
https://railway.app/button.svg

Configuration des variables Railway
Variable	Description	Valeur recommandée
BINANCE_API_KEY	Clé API Binance	
BINANCE_SECRET_KEY	Clé secrète Binance	
BINANCE_TESTNET	Utiliser le testnet	true
PORT	Port d'écoute	5000
WEBHOOK_SECRET	Secret pour signer les webhooks	[Générez avec openssl rand -hex 32]
STRATEGY_TYPE	Type de stratégie	pine
DEFAULT_STRATEGY	Stratégie par défaut	rsi_strategy
DEFAULT_SYMBOL	Symbole par défaut	BTCUSDT
STRATEGY_SCHEDULE	Planification d'exécution	*/5 * * * *
Utilisation
Endpoints API
GET / : Tableau de bord

POST /webhook : Exécuter une stratégie (requiert signature HMAC)

GET /strategies : Liste des stratégies disponibles

GET /performance : Données de performance

GET /logs : Flux de logs en temps réel

Exemple de webhook
python
import requests
import hmac
import hashlib
import json

url = "https://votre-app.railway.app/webhook"
secret = "WEBHOOK_SECRET"
payload = {
    "strategy": "rsi_strategy",
    "symbol": "BTCUSDT"
}

# Calculer la signature
signature = hmac.new(
    secret.encode(),
    json.dumps(payload).encode(),
    hashlib.sha256
).hexdigest()

# Envoyer la requête
headers = {"Content-Type": "application/json", "X-Signature": signature}
response = requests.post(url, json=payload, headers=headers)
Ajouter une nouvelle stratégie
Placez votre fichier .pine dans strategies/pine_strategies/

Le nom du fichier (sans extension) sera le nom de la stratégie

Redémarrez l'application ou envoyez un webhook avec le nouveau nom

Développement
Structure des fichiers
text
bibliotheque/
├── app.py
├── config/
├── core/
├── strategies/
├── templates/           # Fichiers HTML du dashboard
├── static/              # CSS/JS/Images
├── webhooks/
├── requirements.txt
├── Procfile
├── railway.json
└── README.md
Exécution locale
bash
pip install -r requirements.txt
python app.py
Accéder au tableau de bord: http://localhost:5000

Auteur
Ahmed Choukri

Licence
MIT License

Bibliothèque de Stratégies de Trading Automatisé - Guide Complet
markdown
# Bibliothèque de Stratégies de Trading Automatisé

![Dashboard](https://via.placeholder.com/800x400?text=Tableau+de+bord+professionnel)

Plateforme complète pour automatiser l'exécution de stratégies de trading sur Binance, avec tableau de bord professionnel et gestion avancée des stratégies.

## Table des matières
- [Introduction](#introduction)
- [Structure du projet](#structure-du-projet)
- [Déploiement initial](#déploiement-initial)
- [Ajout et gestion des stratégies](#ajout-et-gestion-des-stratégies)
- [Utilisation du tableau de bord](#utilisation-du-tableau-de-bord)
- [Configuration avancée](#configuration-avancée)
- [Dépannage](#dépannage)
- [FAQ](#faq)
- [Astuces professionnelles](#astuces-professionnelles)

## Introduction

Cette plateforme vous permet d'automatiser l'exécution de stratégies de trading écrites en Pine Script sur Binance. Le système inclut :

- 🚀 Exécution automatique selon un planning personnalisable
- 📊 Tableau de bord professionnel pour le monitoring
- 🔔 Notifications et alertes en temps réel
- 🔐 Sécurité renforcée avec authentification HMAC
- 📈 Backtesting intégré (en développement)

## Structure du projet
bibliotheque/
├── app.py # Point d'entrée principal
├── config/
│ ├── init.py
│ └── settings.py # Configuration de l'application
├── core/
│ ├── init.py
│ ├── trading_engine.py # Moteur de trading
│ └── pine_executor.py # Exécuteur de stratégies Pine
├── strategies/
│ └── pine_strategies/ # Dossier des stratégies
│ ├── macd_strategy.pine # Exemple de stratégie MACD
│ └── rsi_strategy.pine # Exemple de stratégie RSI
├── webhooks/
│ ├── init.py
│ └── binance_webhook.py # Gestion des webhooks
├── templates/ # Interface utilisateur
│ ├── dashboard.html
│ ├── strategies.html
│ ├── logs.html
│ └── layout.html
├── static/ # Ressources statiques
│ ├── css/
│ │ └── styles.css
│ ├── js/
│ │ └── dashboard.js
│ └── img/
│ └── logo.svg
├── requirements.txt # Dépendances Python
├── Procfile # Configuration Railway
├── railway.json # Configuration du déploiement
└── README.md # Ce fichier

text

## Déploiement initial

### Prérequis
- Compte [GitHub](https://github.com)
- Compte [Railway](https://railway.app)
- Clés API Binance

### Étapes de déploiement

1. **Forker le dépôt**  
   Cliquez sur "Fork" en haut à droite de la [page du dépôt](https://github.com/fellouhahmedchoukri/bibliotheque)

2. **Déployer sur Railway**  
   [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/fellouhahmedchoukri/bibliotheque)

3. **Configurer les variables d'environnement**  
   Dans l'onglet "Variables" de Railway, ajoutez:

   | Variable | Valeur | Description |
   |----------|--------|-------------|
   | `BINANCE_API_KEY` | Votre clé API | Clé API Binance |
   | `BINANCE_SECRET_KEY` | Votre clé secrète | Clé secrète Binance |
   | `BINANCE_TESTNET` | `true` | Utiliser le testnet pour les tests |
   | `PORT` | `5000` | Port d'écoute de l'application |
   | `WEBHOOK_SECRET` | `openssl rand -hex 32` | Secret pour signer les webhooks |
   | `STRATEGY_TYPE` | `pine` | Type de stratégie |
   | `DEFAULT_STRATEGY` | `rsi_strategy` | Stratégie par défaut |
   | `DEFAULT_SYMBOL` | `BTCUSDT` | Paire de trading par défaut |
   | `STRATEGY_SCHEDULE` | `*/5 * * * *` | Exécution toutes les 5 minutes |

4. **Accéder à l'application**  
   Une fois déployé, accédez à votre application via le domaine fourni par Railway.

## Ajout et gestion des stratégies

### Format des stratégies Pine Script
Les stratégies doivent être au format Pine Script v5. Exemple de stratégie RSI:

```pine
//@version=5
strategy("RSI Strategy", overlay=true)

length = input(14, "RSI Length")
oversold = input(30, "Oversold")
overbought = input(70, "Overbought")

rsi = ta.rsi(close, length)
buySignal = ta.crossover(rsi, oversold)
sellSignal = ta.crossunder(rsi, overbought)

if (buySignal)
    strategy.entry("Buy", strategy.long)

if (sellSignal)
    strategy.entry("Sell", strategy.short)
Ajouter une nouvelle stratégie
Créez votre fichier .pine (ex: ema_crossover.pine)

Placez-le dans le dossier strategies/pine_strategies/

Poussez les changements sur GitHub:

bash
git add strategies/pine_strategies/ema_crossover.pine
git commit -m "Ajout de la stratégie EMA Crossover"
git push origin main
Railway déploiera automatiquement la nouvelle version

Activer une stratégie
Via les variables d'environnement:

Modifiez DEFAULT_STRATEGY avec le nom de votre fichier sans extension

Ex: ema_crossover

Via le tableau de bord:

Accédez à /strategies

Cliquez sur l'icône "Activer" à côté de votre stratégie

Tester une stratégie
bash
# Tester localement
python -c "from core.pine_executor import PineExecutor; p = PineExecutor(); print(p.execute_strategy('ema_crossover', 'ETHUSDT'))"

# Tester via API
curl -X POST https://votre-app.railway.app/api/strategies/ema_crossover/execute
Utilisation du tableau de bord
Navigation principale
Dashboard - Vue d'ensemble des performances

Stratégies - Gestion des stratégies

Logs - Surveillance en temps réel

Paramètres - Configuration du système

Fonctionnalités clés
Dashboard
Graphique de performance historique

Dernières exécutions avec résultats

Statut du système en temps réel

Actions rapides:

Exécuter manuellement une stratégie

Ajouter une nouvelle stratégie

Accéder aux logs

Gestion des stratégies
https://via.placeholder.com/800x400?text=Interface+Gestion+Strat%C3%A9gies

Liste des stratégies disponibles

Filtres par statut (actif/inactif)

Actions:

▶️ Exécuter immédiatement

⏯️ Activer/Désactiver

🗑️ Supprimer

Bouton "Ajouter une stratégie" pour uploader de nouveaux scripts

Logs en temps réel
Flux continu des logs système

Option de défilement automatique

Bouton pour effacer les logs

Filtrage par niveau (INFO, WARNING, ERROR)

Recherche textuelle

Exécution manuelle
Allez dans "Stratégies"

Trouvez votre stratégie

Cliquez sur l'icône "Play" (▶️)

Surveillez les résultats dans les logs

Configuration avancée
Personnaliser la planification
Modifiez la variable STRATEGY_SCHEDULE avec une expression cron:

Planification	Expression	Description
Toutes les 5 minutes	*/5 * * * *	Défaut
Toutes les heures	0 * * * *	À chaque heure
Quotidiennement	0 12 * * *	Tous les jours à 12h00
Personnalisée	15 8-18 * * 1-5	À 8h15, 9h15,...,18h15 du lundi au vendredi
Webhooks sécurisés
Pour déclencher une stratégie via un webhook externe:

python
import requests
import hmac
import hashlib
import json

url = "https://votre-app.railway.app/webhook"
secret = "VOTRE_WEBHOOK_SECRET"
payload = {
    "strategy": "macd_strategy",
    "symbol": "SOLUSDT",
    "action": "buy"  # Paramètre optionnel
}

# Calculer la signature HMAC
signature = hmac.new(
    secret.encode(),
    json.dumps(payload).encode(),
    hashlib.sha256
).hexdigest()

# Envoyer la requête
headers = {
    "Content-Type": "application/json",
    "X-Signature": signature
}

response = requests.post(url, json=payload, headers=headers)
print(response.status_code, response.text)
Intégration avec TradingView
Créez une alerte dans TradingView

Configurez le webhook:

text
URL: https://votre-app.railway.app/webhook
Méthode: POST
Headers:
  Content-Type: application/json
  X-Signature: {{VOTRE_SIGNATURE}}
Corps:
{
  "strategy": "votre_strategie",
  "symbol": "{{ticker}}",
  "action": "{{strategy.order.action}}"
}
Dépannage
Problèmes courants
Stratégie non trouvée

Vérifiez le nom du fichier dans strategies/pine_strategies/

Vérifiez la variable DEFAULT_STRATEGY

Consultez les logs pour le chemin exact des stratégies

Erreurs d'API Binance

Vérifiez vos clés API dans Railway

Assurez-vous que BINANCE_TESTNET est correct

Vérifiez les permissions des clés API

Webhook non authentifié

Vérifiez le WEBHOOK_SECRET

Assurez-vous de calculer correctement la signature HMAC

Utilisez le même corps de requête pour la signature

Données manquantes dans le tableau de bord

Actualisez la page

Vérifiez la connexion au serveur

Consultez les logs pour les erreurs d'API

Commandes utiles
bash
# Voir les logs Railway
railway logs

# Tester localement
python app.py

# Vérifier les dépendances
pip install -r requirements.txt

# Lancer un shell dans le conteneur
railway run bash
FAQ
Q: Puis-je utiliser d'autres langages que Pine Script?
R: Oui! Modifiez STRATEGY_TYPE et ajoutez des exécuteurs pour Python, JavaScript, etc.

Q: Comment augmenter la fréquence d'exécution?
R: Modifiez STRATEGY_SCHEDULE (ex: */2 * * * * pour toutes les 2 minutes).

Q: Puis-je exécuter plusieurs stratégies simultanément?
R: Oui, utilisez des webhooks différents ou modifiez le scheduler pour appeler plusieurs stratégies.

Q: Comment sauvegarder mes stratégies?
R: Toutes les stratégies sont dans votre dépôt GitHub, elles sont donc sauvegardées automatiquement.

Q: Est-ce que je peux utiliser ce système en production?
R: Oui, mais commencez toujours par le testnet et avec des montants modestes.

Astuces professionnelles
Journalisation avancée
Ajoutez des logs détaillés dans vos stratégies:

python
logger.info(f"Signal d'achat détecté sur {symbol} à {current_price}")
Notifications
Intégrez des notifications Telegram ou Email:

python
def send_telegram_message(message):
    requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", json={
        "chat_id": CHAT_ID,
        "text": message
    })
Backtesting
Ajoutez un endpoint pour le backtesting:

python
@app.route('/backtest', methods=['POST'])
def backtest_strategy():
    # Implémentez le backtesting ici
    return jsonify(results)
Sécurité renforcée
Ajoutez une liste blanche d'IP:

python
@app.before_request
def limit_remote_addr():
    allowed_ips = ['192.168.1.0/24']
    if request.remote_addr not in allowed_ips:
        return "Accès non autorisé", 403
Monitoring avancé
Intégrez Prometheus pour le monitoring:

python
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)
Ce système vous offre une solution complète pour automatiser vos stratégies de trading tout en fournissant une interface professionnelle pour surveiller et gérer vos opérations. Pour toute question supplémentaire, consultez les issues GitHub ou ouvrez une nouvelle discussion.

text

Ce fichier README.md complet contient toutes les informations nécessaires pour déployer, configurer et utiliser votre système de trading automatisé, avec des explications détaillées sur chaque fonctionnalité et des astuces professionnelles pour optimiser votre utilisation.
