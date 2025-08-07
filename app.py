import os
import logging
from flask import Flask

# Configuration du logging
logging.basicConfig(level=logging.DEBUG)

# Création de l'application Flask
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-for-inventory")

# Import des routes après la création de l'app pour éviter les imports circulaires
from routes.main_routes import main_bp
from routes.product_routes import product_bp
from routes.movement_routes import movement_bp
from routes.statistics_routes import statistics_bp

# Enregistrement des blueprints
app.register_blueprint(main_bp)
app.register_blueprint(product_bp, url_prefix='/produits')
app.register_blueprint(movement_bp, url_prefix='/mouvements')
app.register_blueprint(statistics_bp, url_prefix='/statistiques')
