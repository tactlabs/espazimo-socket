from flask import Flask , render_template
from flask_socketio import SocketIO, emit
import random
import json

app = Flask(__name__)

socketio = SocketIO(app)

@app.route("/jestor", methods = ['GET', 'POST'])
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
def message(jestor_push, methods = ['GET']):
    #print(json)
    jestor_push = dict_formatter(jestor_push)
    write_json(jestor_push)
    socketio.emit('message_response', jestor_push)

# def update_json(data):
#     json_file = open("questions.json")
#     json_data = json.load(json_file)
#     json_data.update(data)
#     with open('questions.json','w') as questions :
#         json.dump(json_data,questions)
#     return 0

def dict_formatter(data):
    new_dict = {
	data["q_number"] : {
		"question" : data["question"],
		"options1" : data["option_1"],
        "options2" : data["option_2"],
        "options3" : data["option_3"],
        "options4" : data["option_4"],
        "answer"   : data["answer"]
    }
		
	}

    return new_dict


def write_json(new_data, filename='questions.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data["questions"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)
 
    # python object to be appended.


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

# def random_name():
#     names = ['stupendous_saturn', 'jolly_jupiter', 'marvelous_mars']

#     n = random.randint(0,2)

#     return names[n]



if __name__ == '__main__':
    socketio.run(app, debug = True)
