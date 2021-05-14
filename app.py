from flask import Flask , render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)

socketio = SocketIO(app)

@app.route("/admin", methods = ['GET', 'POST'])
def admin():
    return render_template("index.html")

@app.route("/", methods = ['GET', 'POST'])
def index():
    return render_template("message.html")

@socketio.on('connect')
def connected():
    print('connect')

@socketio.on('sms')
def message(json, methods = ['GET']):
    #print(json)
    socketio.emit('message_response', json)

@socketio.on('check')
def message(json, methods = ['GET']):
    # print(json)
    socketio.emit('message_response', json)   
    socketio.emit('answer_response', json) 

if __name__ == '__main__':
    socketio.run(app, debug = True)
