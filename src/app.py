from flask import Flask, render_template
from flask_mysqldb import MySQL
from config import config

app = Flask (__name__)

conexion = MySQL(app)

@app.route('/', methods=['GET'])

def index ():
        try:
            cursor = conexion.connection.cursor()
            sql = "SELECT c.Name AS Pais, ci.Name AS Capital FROM country c JOIN city ci ON c.capital = ci.ID;"
            cursor.execute(sql)
            datos = cursor.fetchall()
            dato = []
            for fila in datos:
                user = {
                      'Pais' : fila [0],
                      'Capital': fila [1]

                      }
                dato.append(user)            
            return render_template('index.html', dic=dato)
        except Exception as ex:
            return ('Error en la consulta a la BD')  
              
def pagina_no_encontrada(error):
    return "<h1> Pagina no encontrada</h1>",484

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(debug =True, port=3000)


 




