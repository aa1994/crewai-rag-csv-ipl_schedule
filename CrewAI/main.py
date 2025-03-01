from crew import IPLCrew
from flask import Flask, request, render_template
from flask_cors import CORS


# initialize Flask server
app = Flask(__name__)
CORS(app)


history = []

def addtoHistory(message, user):
    json_to_append = {
        'role': user,
        'text': message
    }
    history.append(json_to_append)
    print(history)
    return history

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/api/chat", methods=["POST"])
def home():
    data = request.get_json()
    message = data['message']
    history = addtoHistory(message, 'user')
    crew_response = callCrew(message,history)
    return {"answer_response": crew_response["answer_response"]}

def callCrew(message,history):
    inputs = {
        "input_from_user":message,
        "history":history
    }
    crew_response =  IPLCrew().iplCrew().kickoff(inputs=inputs)
    addtoHistory(crew_response["answer_response"], 'model')
    return crew_response

if __name__ == "__main__":
    app.run(debug=True)