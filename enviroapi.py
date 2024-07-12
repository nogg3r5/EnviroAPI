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

#http://192.168.4.48:5000/average?days=3&time=h or d or m
#select AVG(temp),datetime from Enviro where datetime>= datetime('now','-180 day','localtime') group by strftime('%YYYY-%mmm-%dd %HH', datetime);
@app.route('/average', methods= ['GET'])
def average():
 days = flask.request.args.get('days', default=180, type = float)
 days = "'-"+str(days)+" day'"
 time = flask.request.args.get('time', default='d')
 if time == 'd':
  time = '%YYYY-%mmm-%dd'
 elif time == 'h':
  time = '%YYYY-%mmm-%dd %HH'
 elif time == 'm':
  time = '%YYYY-%mmm'
 else:
  time = '%YYYY-%mmm-%dd'
 sqliteConnection = sqlite3.connect('/home/pi/database/enviro.db')
 query = "select AVG(temp),datetime from Enviro where datetime>= datetime('now',"+days+",'localtime') group by strftime('"+time+"', datetime);"
 cursor = sqliteConnection.cursor()
 cursor.execute(query)
 data = cursor.fetchall()
 cursor.close()
 sqliteConnection.close()
 return flask.jsonify(data)

@app.route('/upload')
def my_form():
    return flask.render_template('upload.html')

@app.route('/upload', methods=['POST'])
def my_form_post():
    text = flask.request.form['text']
    type = flask.request.form['type']
    print(text)
    print(type)
    with open("links.txt", "a") as fo:
     fo.write(text+","+type+"\n")
    return flask.render_template('upload.html')

#http://192.168.4.48:5000/uploadurl/https://google.co.uk
@app.route('/uploadurl/<path:input_url>')
def UploadURL(input_url):
    url = input_url
    with open("links.txt", "a") as fo:
     fo.write(url +"\n")
    return url

app.run(host='0.0.0.0')
