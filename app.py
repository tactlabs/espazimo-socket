
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

# Business 

FILEPATH                = 'questions.json'
FIRST_ROUND_BASE_SCORE  = 5

def get_json_data():

    with open(FILEPATH) as json_file:
        data = json.load(json_file)
        
        # print(data)

    return data

def store_json_data(data):

    with open(FILEPATH, 'w') as outfile:
        json.dump(data, outfile)

def add_question(question_dict):

    q_number    = question_dict['q_number']
    q_json      = get_json_data()

    q_json[q_number]    = question_dict

    store_json_data(q_json)

def add_team_answer(q_number, team_name, answer):

    q_json      = get_json_data()

    current_q_json = q_json[q_number]

    # team_answer_dict = current_q_json['team_answers']

    if('team_answers' not in current_q_json):
        # create a new
        current_q_json['team_answers'] = {}

    current_q_json['team_answers'][team_name] = answer

    store_json_data(q_json)

def add_team_score(q_number, team_name, score):

    q_json      = get_json_data()

    current_q_json = q_json[q_number]

    # team_answer_dict = current_q_json['team_answers']

    if('score' not in current_q_json):
        # create a new
        current_q_json['score'] = {}

    current_q_json['score'][team_name] = score

    store_json_data(q_json)

def is_correct_answer(q_number, my_answer):

    q_json      = get_json_data()

    current_q_json = q_json[q_number]

    base_answer = current_q_json['answer']
    base_answer = base_answer.lower()
    
    my_answer = my_answer.lower()

    if(my_answer == base_answer):
        return True

    return False

def updated_leaderboard(team_name, current_score):

    q_json      = get_json_data()

    if('leaderboard' not in q_json):
        # create a new
        q_json['leaderboard'] = {}

    leaderboard_json = q_json['leaderboard']

    if(team_name not in leaderboard_json):
        leaderboard_json[team_name] = 0

    current_score = int(current_score)

    leaderboard_json[team_name] = int(leaderboard_json[team_name]) + current_score

    store_json_data(q_json)

def get_leaderboard():

    q_json      = get_json_data()

    if('leaderboard' not in q_json):
        result = {
            'error_code'    : 1892,
            'error_message' : 'Result Not Available'
        }

        return result

    # sorted_leadboard = sort_dict_reverse(q_json['leaderboard'])

    result = {
        'error_code'    : 0,
        'error_message' : 'NA',

        'leaderboard'   : q_json['leaderboard']
    }

    return result

def sort_dict_reverse(mydic):

    mydict = sorted(mydic, key = mydic.get, reverse = True)

    # for w in sorted(mydic, key = mydic.get, reverse = True):
    #     print(w, mydic[w])

    return mydict

##### API / Socket #####

@app.route("/jestor", methods = ['GET', 'POST'])
def admin():
    
    return render_template("admin.html")

@app.route("/", methods = ['GET', 'POST'])
def index():
    
    return render_template("home.html")

@app.route("/audience", methods = ['GET', 'POST'])
def page_audiece():
    
    return render_template("participant.html")

@app.route("/public", methods = ['GET'])
def page_public():
    
    return render_template("public.html")

@socketio.on('connect')
def connected():
    
    print('connect')

@socketio.on('push-question')
def message(question_json, methods = ['GET']):
    #print(json)

    add_question(question_json)

    print('Questions added')
    
    socketio.emit('get-question', question_json)

def format_dictionary(data):
    
    new_dict = {
        data["q_number"] : data
	}

    return new_dict


def get_question(q_number):

    q_json = get_json_data()

    return q_json[q_number]

@socketio.on('submit-answer')
def message(json, methods = ['GET']):
    
    # print(json)  

    # add_team_answer
    q_number    = json['q_number']
    team_name   = json['team_name']
    answer      = json['answer']
    add_team_answer(q_number, team_name, answer)

    # add team score
    current_score = 0

    if(is_correct_answer(q_number, answer)):
        current_score = FIRST_ROUND_BASE_SCORE
        
    
    add_team_score(q_number, team_name, current_score)
    updated_leaderboard(team_name, current_score)

    socketio.emit('submit-answer-to-admin', json) 

@socketio.on('reveal-answers')
def message(json, methods = ['GET']):
    
    #print(json)

    # Get the question details with answer and then publish it
    q_number = json['q_number']

    question_dict = get_question(q_number)

    question_dict['leaderboard'] = get_leaderboard()

    # print('[reveal-answers] : ', question_dict)

    socketio.emit('reveal-answers', question_dict)

@socketio.on('get-leaderboard')
def sock_get_leaderboard(json, methods = ['GET']):

    result = get_leaderboard()

    socketio.emit('get-leaderboard', result)

if __name__ == '__main__':

    socketio.run(app, debug = True)