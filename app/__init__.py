import os
from flask import Flask,jsonify,render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__,static_url_path='/assets', static_folder='assets',template_folder='templates')
    from . import views,api
    app.register_blueprint(views.bp)
    app.register_blueprint(api.bp)
    return app