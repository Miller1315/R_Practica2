from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import config


app = Flask (__name__)

conexion = MySQL(app)

@app.route('/', methods=['GET'])

def index ():
        try:
            cursor = conexion.connection.cursor()
            sql = "SELECT c.Name AS Pais, ci.ID AS ID_Ciudad, ci.Name AS Capital FROM country c JOIN city ci ON c.capital = ci.ID;"
            cursor.execute(sql)
            datos = cursor.fetchall()
            dato = []
            for fila in datos:
                user = {
                      'Pais' : fila [0],
                      'id_capital' : fila [1],
                      'Capital': fila [2]

                      }
                dato.append(user)            
            return jsonify({'dato': dato, 'mensaje': "Listar usuarios", 'confirm': True})
        except Exception as ex:
            return jsonify({'mensaje': "Error en la consulta a la BD", 'confirm': False}) 
        
def leer_usuario_porID (id):
        try:
            cursor = conexion.connection.cursor()
            sql = "SELECT c.Name AS Pais, ci.ID AS ID_Ciudad, ci.Name AS Capital FROM country c JOIN city ci ON c.capital = ci.ID WHERE id = '{0}'".format(id)
            cursor.execute(sql)
            datos = cursor.fetchone()
            if datos != None:
                 dato= {'Pais': datos[0], 'ID_Capital': datos [1], 'Capital': datos [2]}
                 return dato
            else:
                 return None
        except Exception as ex:
            raise ex
              
@app.route('/<id>', methods=['GET'])
def leer_usuario(id):
     try:
          usuario =leer_usuario_porID(id)
          if usuario != None :
               return jsonify ({'usuario': usuario, 'mensaje': 'usuario encontrado', 'confirm': True})
          else:
               return jsonify({'mensaje': 'usuario No encontrado', 'confirm': False})
     except Exception as ex:
          return jsonify({'mensaje': "Error", 'confirm': False})
     
     
@app.route('/', methods=['POST'])
def agregar():
    # if(validateEmail(request.json['email']) and validatePass(request.json['pass'])):
    try:
        usuario = leer_usuario_porID(request.json['id'])
        if usuario != None:
            return jsonify({'mensaje' : 'Error ya existe el ID','confirm': False})
        else:
            cursor= conexion.connection.cursor()

 
            # sql = "INSERT INTO country,city (pais, capital_nombre, capital_id) VALUES ('{0}', '{1}', {2})".format(request.json['pais'], request.json['capital_nombre'], request.json['capital_id'])

            #sql = "INSERT INTO c.Name AS Pais, ci.ID AS ID_Ciudad, ci.Name AS Capital FROM country c JOIN city ci ON c.capital = ci.ID WHERE id = '{0}'".format(id)

            cursor.execute(sql)
            conexion.connection.commit()
            return jsonify({'mensaje':'usuario registrado','confirm': True})
    except Exception as ex:
        return jsonify({'mensaje': 'Error usuario no registrado','confirm':False})   
    # else:
    #     return jsonify({'mensaje': 'Valores no validos', 'confirm':False})




def eliminar_usuario_porID(id):
    try:
        cursor = conexion.connection.cursor()
        # sql = "DELETE FROM city WHERE id = '{0}'".format(id)
        # sql = "DELETE c.Name AS Pais, ci.ID AS ID_Ciudad, ci.Name AS Capital FROM country c JOIN city ci ON c.capital = ci.ID WHERE id  = '{0}'".format(id)

        # sql = "DELETE Pais, city FROM Pais JOIN city ON Pais.ID_Capital = city.ID = '{0}'".format(id)
        sql = "DELETE country, city FROM country JOIN city ON country.capital = city.Name WHERE city.ID = '{0}'".format(id)
    
    
        cursor.execute(sql)
        conexion.connection.commit()
        return True
    except Exception as ex:
        raise ex

@app.route('/<id>', methods=['DELETE'])
def eliminar_usuario(id):
    try:
        usuario = leer_usuario_porID(request.json['id'])
        if eliminar_usuario_porID(id):

            if usuario == None:
                return jsonify({'mensaje': 'No se encontró el usuario', 'confirm': False})
            else:
                return jsonify({'mensaje': 'Usuario eliminado correctamente', 'confirm': True})
            
    except Exception as ex:
        return jsonify({'mensaje': 'Error al eliminar el usuario', 'confirm': False})





def pagina_no_encontrada(error):
    return "<h1> Pagina no encontrada</h1>",484

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug =True, port=3000)


 




