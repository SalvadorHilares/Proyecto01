from operator import sub
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
from sqlalchemy import sql

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:syncmaster750s@localhost:5432/subasta'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
#migrate = Migrate(app, db)

# AQUI VAN LAS ENTIDADES
class Usuario(db.Model):
    __tablename__ = 'usuario'
    dni = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    contraseña = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    dinero = db.Column(db.Integer, default=0)

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    caracteristicas = db.Column(db.String(300), default='')
    precio_inicial = db.Column(db.Integer, nullable=False)
    precio_final = db.Column(db.Integer, default=precio_inicial)
    subasta_id = db.Column(db.Integer, db.ForeignKey('subasta.id'),nullable=False)
    dni_usuario = db.Column(db.Integer, db.ForeignKey('usuario.dni'),nullable=False)
    vendido = db.relationship("Subasta", backref="list", lazy=True)
    posteado = db.relationship("Usuario", backref="list", lazy=True)

class Subasta(db.Model):
    __tablename__ = 'subasta'
    id = db.Column(db.Integer,primary_key=True)
    Hora_inicio = db.Column(db.Date,nullable=False)
    Hora_final = db.Column(db.Date,nullable=False)
 
class Empleado(db.Model):
    __tablename__ = 'empleado'
    dni = db.Column(db.Integer,primary_key=True)
    nombre = db.Column(db.String(80), nullable=False)
    sueldo = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(80), nullable=False)
    id_subasta = db.Column(db.Integer, db.ForeignKey('subasta.id'),nullable=False)
    url = db.Column(db.String(300))

#AQUI VAN LAS RELACIONES
class Participar(db.Model):
    __tablename__ = 'participar'
    pagar = db.Column(db.Integer, default=0)
    ganador = db.Column(db.String(80))
    dni_usuario = db.Column(db.Integer, db.ForeignKey('usuario.dni'),primary_key=True)
    id_subasta = db.Column(db.Integer, db.ForeignKey('subasta.id'),primary_key=True)

db.create_all()

#REGISTRAR USUARIOS
@app.route('/users/create', methods = ['POST'])
def create_user():
    error = False
    response = {}
    try:
        dni = request.get_json()['DNI']
        name = request.get_json()['name']
        password = request.get_json()['password']
        email = request.get_json()['email']
        user = Usuario(dni=dni,nombre=name,contraseña=password,email=email)
        db.session.add(user)
        db.session.commit()
        response['name'] = user.nombre
        response['password'] = user.contraseña
        response['email'] = user.email
        response['dni'] = user.dni
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        response['error_message'] = "[BE] - something went wrong"
    response['error'] = error
    return jsonify(response)
 
#LOGEAR USUARIOS
@app.route('/authenticate/login', methods=['POST'])
def authenticate_user():
    error = False
    response = {}
    try:
        username = request.get_json()['username']
        password = request.get_json()['password']
        user = db.session.query(Usuario).filter(Usuario.nombre==username).filter(Usuario.contraseña==password).one()
        response['dni'] = user.dni
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        response['error_message'] = "Usuario o contraseña incorrecto"
    response['error'] = error
    return jsonify(response)

#POSTEAR PRODUCTOS
@app.route('/publish/product', methods=['POST'])
def publish_product():
    error = False
    response = {}
    try:

        ti = request.get_json()['TI']
        tf = request.get_json()['TF']
        subasta = Subasta(Hora_inicio=ti,Hora_final=tf)
        db.session.add(subasta)
        db.session.commit()

        name = request.get_json()['name']
        price = request.get_json()['price']
        features = request.get_json()['features']
        dni = request.get_json()['DNI']

        product = Producto(nombre=name,caracteristicas=features,precio_inicial=price,subasta_id=subasta.id,dni_usuario=dni)
        db.session.add(product)
        db.session.commit()

        response['name'] = product.nombre
        response['price'] = product.precio_inicial
        response['features'] = product.caracteristicas
        response['id'] = product.id
        
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        response['error_message'] = 'No se pudo ingresar a la base de datos'
    response['error'] = error
    return jsonify(response)

#DELETE PRODUCTOS
@app.route('/product/<product_id>/delete-product', methods=['DELETE'])
def delete_producto_by_id(product_id):
    response = {}
    error = False
    try:
        producto = Producto.query.get(product_id)
        if producto is None:
            response['error_message'] = 'product_id does not exists in the subasta'
        db.session.delete(producto)
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    response['success'] = error
    return jsonify(response)

'''
#EDITAR UN PRODUCTO
@app.route('/product/<product_id>/edit-product', methods=['PUT'])
def edit_product_by_id(product_id):
    response = {}
    error = False
    try:
        id = Producto.query.get(product_id)
        user = db.session.query(Producto).filter(Producto.id==id).first()
        db.session.execute(sql,(user.name,user.price,user.features))
        db.session.commit()
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    response['error'] = error
    return jsonify(response)
'''
@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/homepage/<dni>')
def homepage(dni):
    return render_template('homepage.html',data=Usuario.query.filter_by(dni=dni).first())

@app.route('/products/<dni>')
def products(dni):
    return render_template('products.html',data=Producto.query.all(),data2=Usuario.query.filter_by(dni=dni).first())

if __name__ == '__main__':
    app.run(port=5003, debug=True)
else:
    print('using global variables from FLASK')