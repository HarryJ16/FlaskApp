from flask import (
    Blueprint, render_template, request, url_for, redirect, flash, session, g
    )
#from werkzeug.security import generate_password_hash, check_password_hash
from storeguitar import mysql
import bcrypt


auth_bp= Blueprint('auth',__name__, url_prefix='/auth')

@auth_bp.route('register/', methods =('GET','POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        #Verificar si hay un usuario con el mismo email
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email_user = %s", (email,))
        user = cursor.fetchone()

        error = None

        if user == None:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO users (name_user, email_user, password) VALUES (%s, %s, %s)", (username, email, hashed_password))

            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('auth.login'))
        else:
            error = f'El email {email} ya esta registrado.'
            flash(error)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth_bp.route('login/', methods =('GET','POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = None
        
        #Buscar los datos de la cuenta
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email_user = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        #Validar si el usuario existe
        if user == None:
            error = 'Email incorrecto o no existe'
        elif not bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):
            error = 'Contraseña invalida'

        #print(user)

        #Iniciar Sesion con el usuario
        if error is None:
            session.clear()
            session['user_id'] = user[0]
            return redirect(url_for('todo.listar_guitarra'))
        flash(error)   
    return render_template('auth/login.html')

@auth_bp.route('/check_db_connection')
def check_db_connection():
    try:
        # Intentar obtener un cursor para verificar la conexión
        cursor = mysql.connection.cursor()
        cursor.close()
        return "La conexión a la base de datos está establecida correctamente."
    except Exception as e:
        return f"Error al intentar establecer la conexión a la base de datos: {e}"

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("Has finalizado sesion correctamente.")
    return redirect(url_for('index'))

#Funcion para que se ejecute en cada peticion
@auth_bp.before_app_request
def load_logged_in_user():
    #recupero el id del usuario
    user_id = session.get('user_id')
    # no encuentra usuario logeado
    if user_id is None:
        g.user = None

    else:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id_user = %s", (user_id,))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data:
            user_dict = {
                'id': user_data[0],
                'name': user_data[1],
                'email': user_data[2],
            }
        g.user = user_dict

import functools
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login')) 
        return view(**kwargs)
    return wrapped_view