from flask import Flask

def create_app():
    """Creates and configures the Flask application."""
    app = Flask(__name__)

    with app.app_context():
        from . import routes
        app.register_blueprint(routes.api_bp) # use app.add_url_rule if not using Blueprints

    return app