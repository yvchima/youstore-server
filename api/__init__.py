from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    @app.route('/api/ping')
    def ping():
        return {"message": "Ping!"}

    # Register Blueprint
    from api.errors import errors
    app.register_blueprint(errors)
    from api.routes.auth import auth
    app.register_blueprint(auth)
    from api.routes.users import users
    app.register_blueprint(users)
    from api.routes.products import products
    app.register_blueprint(products)

    from api import models
    
    return app
