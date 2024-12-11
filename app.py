from flask import Flask
from modelos import create_tables
from flask_login import LoginManager
from usuario import Usuario
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pgn', 'jpg', 'jpeg'}

app.secret_key = os.urandom(24).hex()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.get_or_none(Usuario.id == user_id)

create_tables()

from views import *

if __name__ == "__main__":
    app.run(debug=True)