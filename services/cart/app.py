from flask import Flask
from .routes.cart_routes import cart_blueprint
import logging

logging.basicConfig(level=logging.INFO)

def create_app():
    app = Flask(__name__)
    app.config.from_object('services.cart.config.Config')
    app.register_blueprint(cart_blueprint)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5001, debug=True)
