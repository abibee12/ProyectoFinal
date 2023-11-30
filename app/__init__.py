# app/__init__.py
from app.config import Config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import config_dict

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    # Initialize the database
    db.init_app(app)

    # Import blueprints/routes
    from app.routes import data_routes

    # Register blueprints
    app.register_blueprint(data_routes)

    return app

# Crear una instancia de la aplicación
app = create_app('development')

# Inicializar Flask-Migrate con la aplicación y la base de datos
migrate.init_app(app, db)

# Agregar configuración de prueba
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:martinez@localhost:5432/AppPythonTest"

# Agregar la configuración de prueba al diccionario
config_dict["testing"] = TestingConfig
