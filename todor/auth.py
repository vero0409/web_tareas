from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g #redirigir a otra pagina o marcar errores en el inicio de session
from werkzeug.security import generate_password_hash, check_password_hash #el programador no puede ver la contraseña de los usurios
from .models import User
from todor import db #base de datos


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods = ('GET', 'POST'))
def register():#compara 
    if request.method == 'POST':
        username = request.form['username'] #recupera lo que se puso en el campo de el formulario user name se almacena en los campos
        password = request.form['password'] #y esta recupera los campos de las variables 

        user = User(username, generate_password_hash(password)) #genera objeto con las dos variables que sostendran dos cmpos

        error = None #para no tener usuarios repetidos

        user_name = User.query.filter_by(username = username).first() #filtrar todos los nombre de usuraio que esten igual, si el nombre de usurio ya se encuentra va a mandar un valor de que ya se encuentra, en la base de datos
        if user_name == None: #si no encontró un usuario igual en la base de datos:
            db.session.add(user) #se agrega a ala tabla(base de datos)
            db.session.commit() #se guardan cambios
            return redirect(url_for('auth.login')) #te redirecciona a la página de login(iniciar sesión)
        else:
            error = f'el usuario {username} ya esta registrado'

        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods = ('GET', 'POST') )
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None

        #validar datos
        user = User.query.filter_by(username = username).first()
        if user == None:
            error = 'Nombre de usuario incorrecto'
        elif not check_password_hash(user.password, password):
            error = 'Contraseña incorrecta'

            #Iniciar session
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('todo.index'))
        
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request #registra la función para que se ejecute en cada petición
def load_logged_in_user():
    user_id = session.get('user_id') #si alguien inció session devuelve un valor y si no marca un error

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get_or_404(user_id)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

#para que si no estas en autenticado no puedas ver las tareas
import functools
def loging_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view