from flask import Flask

# Import all 4 tools from our new toolbox
from app.extensions import cache, db, limiter, ma


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///autoshop.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Configure the cache (SimpleCache is great for local development)
    app.config["CACHE_TYPE"] = "SimpleCache"

    # Initialize extensions with the app
    db.init_app(app)
    ma.init_app(app)
    cache.init_app(app)
    limiter.init_app(app)

    # Import and register Blueprints
    from .customer import customer_bp
    from .inventory import inventory_bp
    from .mechanic import mechanic_bp
    from .service_ticket import service_ticket_bp

    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    return app
