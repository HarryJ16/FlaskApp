from flask import Blueprint, render_template, redirect, url_for, request, session, g
from storeguitar.auth import login_required
from storeguitar import mysql

# Nombre del Blueprint, Modulo actual, Rutas definidas dentro del Blueprint
bp = Blueprint('todo',__name__, url_prefix='/storeguitar')


@bp.route('/listar_guitarra')
@login_required
def listar_guitarra():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM guitars")
    guitarras = cursor.fetchall()
    cursor.close()
    return render_template('store/index.html', guitarras = guitarras)

@bp.route('/crear_guitarra', methods=('GET','POST'))
@login_required
def crear_guitarra():
    if request.method == 'POST':

        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']

        cursor = mysql.connection.cursor()
        cursor.execute ("INSERT INTO guitars VALUES (NULL, %s,%s,%s)", (marca, modelo, precio))
        cursor.connection.commit()

        return redirect(url_for('todo.listar_guitarra'))
    return render_template('store/create.html')

@bp.route('/editar_guitarra/<int:id_guitarra>', methods=['GET','POST'])
@login_required
def editar_guitarra(id_guitarra):

    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']

        cursor = mysql.connection.cursor()
        cursor.execute("""
                       UPDATE guitars
                       SET marca=%s, modelo=%s, precio=%s WHERE id_guitarra = %s
                       """, (marca, modelo, precio, id_guitarra))
        mysql.connection.commit()

        return redirect(url_for('todo.listar_guitarra'))

    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM guitars WHERE id_guitarra = {id_guitarra}")
    guitarra = cursor.fetchone()
    cursor.close()

    return render_template('store/editar.html', guitarra=guitarra)

@bp.route('/borrar_guitarra /<int:id_guitarra>')
@login_required
def borrar_guitarra(id_guitarra):
    cursor = mysql.connection.cursor()
    cursor.execute(f"DELETE FROM guitars WHERE id_guitarra={id_guitarra}")
    mysql.connection.commit()

    return redirect(url_for('todo.listar_guitarra'))

@bp.route('/cuenta_user')
@login_required
def cuenta_user():
    user_id = session.get('user_id')

    if 'user_id' in session:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id_user = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        print(user)
        return render_template('store/cuenta_user.html', user = user)
    return render_template('store/cuenta_user.html')
    
