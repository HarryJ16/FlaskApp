from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Configuracion del Proyecto
app.config.from_mapping(
    DEBUG = True,
    SECRET_KEY = 'MiAppSecreta'
)

#Configuration MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'guitarstore'
app.secret_key = 'key321!'
mysql = MySQL(app)

# Registro de BluePrint Todo
from . import todo
app.register_blueprint(todo.bp)

# Registro de BluePrint Auth
from . import auth
app.register_blueprint(auth.auth_bp)



