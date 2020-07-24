from flask import Flask

from .database import db
import app.app_english.controllers as firstmodule

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.BaseConfig')

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    app.register_blueprint(firstmodule.app_english, url_prefix='/english')
    return app


