
'''
Created on 
    March 26, 2021

Course work: 
    Python Snippet Collection

@author: Serkinti Team

Source:
    
'''

# Import necessary modules
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
def message(question_json, methods = ['GET']):
    #print(json)
    
    question_json = format_dictionary(question_json)
    write_json(question_json)
    socketio.emit('message_response', question_json)

# def update_json(data):
#     json_file = open("questions.json")
#     json_data = json.load(json_file)
#     json_data.update(data)
#     with open('questions.json','w') as questions :
#         json.dump(json_data,questions)
#     return 0

def format_dictionary(data):
    
    new_dict = {
        data["q_number"] : data
	}

    return new_dict


def write_json(new_data, filename = 'questions.json'):
    
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
