import flask
import sqlite3

app = flask.Flask(__name__)

@app.route('/', methods= ['GET'])
def index():
 sqliteConnection = sqlite3.connect('/home/pi/database/enviro.db')
 query = """SELECT * from Enviro where datetime>= datetime('now','-1 day');"""
 cursor = sqliteConnection.cursor()
 cursor.execute(query)
 data = cursor.fetchall()
 cursor.close()
 sqliteConnection.close()
 return flask.jsonify(data)

@app.route('/custom', methods=['GET'])
def custom():
 days = flask.request.args.get('days', default=1, type = float)
 days = "'-"+str(days)+" day'"
 sqliteConnection = sqlite3.connect('/home/pi/database/enviro.db')
 query = "SELECT * from Enviro where datetime>= datetime('now',"+days+");"
 cursor = sqliteConnection.cursor()
 cursor.execute(query)
 data = cursor.fetchall()
 cursor.close()
 sqliteConnection.close()
 return flask.jsonify(data)

@app.route('/latest', methods= ['GET'])
def latest():
 sqliteConnection = sqlite3.connect('/home/pi/database/enviro.db')
 query = """SELECT * from Enviro ORDER BY ID DESC LIMIT 1;"""
 cursor = sqliteConnection.cursor()
 cursor.execute(query)
 data = cursor.fetchall()
 cursor.close()
 sqliteConnection.close()
 return flask.jsonify(data)

app.run(host='0.0.0.0')
