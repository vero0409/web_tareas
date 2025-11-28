from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy #se crea aun a extencion 

#Crear una extencion de SQLAlchemy
db = SQLAlchemy()#se crea una extencion y se le agrega a sqlalchemy

def create_app():
    app = Flask(__name__)#se genera la aplicacion
      #configuracion del proyecto

    app.config.from_mapping(
        DEBUG = True,
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI = "sqlite:///todolist.db"#crea y asigna un nombre a la base de datos 
    )

    #Inicializar la conexión de la base de datos
    db.init_app(app)#iniciando la coneccion con la aplicacion 

    #registrar bluet print
    from . import todo 
    app.register_blueprint(todo.bp)
    from . import auth
    app.register_blueprint(auth.bp)

    @app.route("/")#El primer paso antes que nada es crear nuestra ruta principal
    def index():
        return render_template('index.html')
    
    #Por ultimo migrar todos los modelos a la base de datos
    with app.app_context():
        db.create_all()
    
    return app