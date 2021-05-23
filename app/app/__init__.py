import os
from flask import Flask
from flask_restful import  Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)
api = Api(app)
DB_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
DB_HOST = os.getenv('DB_HOST')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:5432/{POSTGRES_DB}"
app.config['SECRET_KEY'] = 'secreGRESPOSTGRw123PASSWORDgoe()23here'

# mail accounts
app.config['MAIL_SERVER'] =  os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = bool(int(os.getenv('MAIL_USE_TLS')))
app.config['MAIL_USE_SSL'] = bool(int(os.getenv('MAIL_USE_SSL')))
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
mail = Mail(app)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
db.init_app(app)
ma = Marshmallow(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


from app import apis, routs , models, auth, errors, utils