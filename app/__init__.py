from flask import Flask

def create_app():
    """Create a Flask app instance"""
    app = Flask(__name__)

    from app.routes.routes import main_bp
    app.register_blueprint(main_bp)

    return app
