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

# AQUI VAN LAS CLASES
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)

class Producto(db.Model):
    __tablename__ = 'producto'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    features = db.Column(db.String(300), default='')
    price = db.Column(db.Integer, nullable=False)

db.create_all()

#REGISTRAR USUARIOS
@app.route('/users/create', methods = ['POST'])
def create_user():
    error = False
    response = {}
    try:
        name = request.get_json()['name']
        password = request.get_json()['password']
        email = request.get_json()['email']
        user = Usuario(name=name,password=password,email=email)
        db.session.add(user)
        db.session.commit()
        response['name'] = user.name
        response['password'] = user.password
        response['email'] = user.email
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
        user = db.session.query(Usuario).filter(Usuario.name==username).filter(Usuario.password==password).one()
        response['username'] = user.name
        response['password'] = user.password
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

#POSTEAR PRODUCTOS
@app.route('/publish/product', methods=['POST'])
def publish_product():
    error = False
    response = {}
    try:
        name = request.get_json()['name']
        price = request.get_json()['price']
        features = request.get_json()['features']
        product = Producto(name=name,features=features,price=price)
        db.session.add(product)
        db.session.commit()
        response['name'] = product.name
        response['price'] = product.price
        response['features'] = product.features
    except:
        error = True
        db.session.rollback()
    finally:
        db.session.close()
    if error:
        response['error_message'] = '[BE] - something went wrong'
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

@app.route('/')
def index():
    return render_template('index.html', data=Usuario.query.all())

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/homepage')
def home_page():
    return render_template('homepage.html')

@app.route('/we')
def we():
    return render_template('we.html')

@app.route('/auction')
def auction():
    return render_template('auction.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/homepage/products')
def products():
    return render_template('products.html',data=Producto.query.all())

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(port=5003, debug=True)
else:
    print('using global variables from FLASK')