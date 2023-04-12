import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from .config import Config

app = Flask(__name__)
csrf = CSRFProtect(app)
app.config.from_object(Config)
app.config['UPLOAD_FOLDER'] = os.path.abspath('./uploads')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cors = CORS(app)

from app import views
from app import models