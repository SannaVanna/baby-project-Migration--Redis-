from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .routes import routes, OrderView
from .db import db

app = Flask(__name__, static_folder="./templates/assets", static_url_path="/assets")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///babyproduct.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


# class FirstView(View):
#    def dispatch_request(self):
#        if request.method == "POST":
#            pass
#        if request.method == "GET":
#            pass
#        return "Hello World"
#    app.add_url_rule('/firstview', view_func=FirstView.as_view('get_request'))


def connect():
    app.secret_key = "grgrgrg"
    app.config['debug'] = True
    app.config['UPLOAD_FOLDER'] = "templates/assets/image"
    app.register_blueprint(routes, url_prefix="/")
    app.add_url_rule('/order/<int:product_id>', view_func=OrderView.as_view('get_request'))


#   app.add_url_rule('/firstview', view_func=FirstView.as_view('get_request'))

    return app
