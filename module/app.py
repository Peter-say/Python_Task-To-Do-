from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set the secret key and other configurations
app.secret_key = "]{\\\xa0\x9e\xb4~\xdf\xd5\xcf\xca\xd6z\xfa2mI\xf3\x96\xd0\xb2\x04\x92\x00"
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/task_manager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True  # For development, to automatically reload templates

app.use_x_sendfile = False

# Initialize the database
db = SQLAlchemy()
db.init_app(app)