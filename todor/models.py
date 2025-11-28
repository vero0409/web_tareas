from todor import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)# un identificador unico, hacer una columna, de tipo entero, viene una llave primaria para saber cuantas tareas a creado ese usuario enlasado con la tabla de tareas 
    username = db.Column(db.String(20), unique = True, nullable = False)#nmbre de usuario, nombre unico, no puede quedar vacio, de tipo strins
    password = db.Column(db.Text, nullable = False)#cadena tipon tento, no puede quedar vacio

    def __init__(self, username, password):#sintesis de un constructos, def como funcion, contiene los campos
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'#reprecenta las tablas

    

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)#se genera un id para generar las tareas

    create_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)#por quien fue creado,columnas,tipo entero, y una llave foranea, nombre de la base de datos y nombre 
    title = db.Column(db.String(100), nullable = False)#tittulo, descripcion puede quedar vacio , steil falso o verdadero 
    desc = db.Column(db.Text)
    state = db.Column(db.Boolean, default = False)#se vuelve a rrepetir el constructor, con los campos, false por que no los toma como verdaderos



    def __init__(self, create_by, title, desc, state = False):
        self.create_by = create_by
        self.title = title
        self.desc = desc
        self.state = state

    def __repr__(self):
        return f'<Todo: {self.title}>'#se reprecenta por su titulo