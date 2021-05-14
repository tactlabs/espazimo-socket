from flask import Flask , render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)

socketio = SocketIO(app)

@app.route("/admin", methods = ['GET', 'POST'])
def admin():
    return render_template("index.html")

@app.route("/", methods = ['GET', 'POST'])
def index():
    return render_template("firstpage.html")

@app.route("/audience", methods = ['GET', 'POST'])
def page_audiece():
    return render_template("participant.html")

@socketio.on('connect')
def connected():
    print('connect')

@socketio.on('push-question')
def message(json, methods = ['GET']):
    #print(json)
    socketio.emit('message_response', json)

@socketio.on('submit-answer')
def message(json, methods = ['GET']):
    print(json)
    # socketio.emit('message_response', json)   
    socketio.emit('submit-answer-to-admin', json) 

@socketio.on('reveal-answers')
def message(json, methods = ['GET']):
    #print(json)

    print('[reveal-answers]')

    result_json = {
        'answer' : 'Toronto'
    }

    socketio.emit('reveal-answers', result_json)

if __name__ == '__main__':
    socketio.run(app, debug = True)
