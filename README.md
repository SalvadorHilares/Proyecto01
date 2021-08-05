# ProyectoWEB

## Página de subasta Integrates:

- Salvador Eliot Hilares Barrios
- Diego Antonio Escajadillo Guerrero
- Alexander Baldeon Medrano
### Descripción del proyecto:

La siguiente página de subasta contiene un login y register para el usuario y para que suban,editen y eliminen sus productos. Está conectado a una base de datos en postgreSQL. El nombre del database es "subasta" y contiene dos tablas con nombres Usuario y Producto. La tabla Usuario tiene cuatro atributos y estas son id, name, password y email. En cambio, la tabla Producto tiene por atributos el id, name, features y price.

### Objetivos principales:

Nuestro principal misión con este trabajo es simular una página de subastas con el fin de comprender como está estructurado una. Nuestro Visión es poder lograr completar la página en su totalidad con una buena relación de base de datos, mejorar nuestra estructura del proyecto y meterla en un buen hosting para que aguante varios transaciones y conexiones.

### Tecnologías usadas:

Las versiones y nombres de las librerías usadas estan en requeriments.txt. Las tecnologías usadas son HTML, JS, CSS y Python.

### Base de datos:

La base de datos tiene que crearse manualmente desde el computador con el nombre "subasta".

### Host:

El host es del puerto del computador

## Descripción de los html en la carpeta templates:

### base.html

Aqui lo único que definimos es la base de las plantillas que heredarán en los otros .html

### login.html

Definimos tres inputs donde los dos primeros son el username y password. Al tener la base de datos virgen, lo primero que hacemos es registrarnos en el link colocado en la parte inferior con el nombre "REGISTRARSE". Si insiste en querer logearse sin ningun usuario existente, entonces botará un mensaje error para avisar al usuario.

### register.html

Pedimos la información básica al usuario como su nombre, correo y contraseña para registrarlo en la base de datos. Otro dato es que en Perú para poder identificar a la persona es el DNI ("Documento Nacional de Identificación"). Esto lo usaremos como si fuera su nuestro id. 

### homepage.html

Una vez logeado, el usuario podrá revisar aquí todas sus acciones que puede realizar en la página. Tales como postear un producto, aumentar dinero a su cartera digital y revisar las subastas que se dan en ese momento. También tiene otro botón donde se podrá hacer LOGOUT para cerrar su sesión.

### products.html

Página donde se podrá postear un producto. Para esto se pedira el nombre, precio inicial, características, tiempo de inicio de la subasta en (aaaa-mm-dd) y tiempo de fin subasta (aaaa-mm-dd).

## archivos .js y .css

### user.js

En este javascript lo único que hacemos es pasar mediante un fetch y un metodo POST al servidor los datos obtenidos por los forms. Una vez regresado el jsonResponse, empezamos a comprobar si fue True o False la respuesta del servidor con el fin de ver que condición cumple (registro aceptado o no).

### product.js

En este javascript hacemos el fecth, metodo POST, DELETE al servidor con tal de ver si agrega o quita un producto subido a la pagina. También hacemos la impresión de los datos desde la base de datos.

### login.js

Solo enviamos los datos del formulario al servidor y luego confirmamos si te lograste logear o no.

## app.py

Es el servidor donde se ejecuta toda la parte de la lógica. Primero esta la definición de las Entidades y las Relaciones. Cada uno con sus foreign keys y primary keys correspondientes. Luego la parte de las rutas y métodos que se harán en la aplicación. Finalmente los render template de las páginas que se usaran las plantillas heredadas
