from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os

# 環境変数を読み込み
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='app.config.DevelopmentConfig'):
  app = Flask(__name__)
  CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

  # Configuration
  app.config.from_object(config_class)

  db.init_app(app)
  migrate.init_app(app, db)

  from app.main import models as main_models

  # Register Blueprints
  from app.main.routes import api
  app.register_blueprint(api)

  # from .auth import auth as auth_blueprint
  # app.register_blueprint(auth_blueprint, url_prefix='/auth')

  return app
