from flask import Flask, request
from flask_socketio import SocketIO, emit

from stablediffusion_dixit.model import GameState

app = Flask(__name__)
socketio = SocketIO(app)

game_state = GameState()

@app.route("/blah", methods=["POST"])
def blah():
    req = request.get_json()
    return {
        "resp": f"Hello, {req['name']}"
    }


@socketio.on("join_game")
def join_game(data):
    print("join game")
    print(data)
    print(request.sid)
    emit("blah", {"a": "Hello " + data["name"]})

@socketio.on("enter_prompt")
def enter_prompt(data):
    prompt_text = data["prompt"]

@socketio.on("active_player_proceed")
def proceed():
    print("proceeding")
    print(request.sid)

@socketio.on("vote")
def vote(data):
    print("vote")
    print(data["voted_for"])
    print(request.sid)

@socketio.on("disconnect")
def disconnect():
    print(request.sid + " disconnected")


if __name__ == "__main__":
    socketio.run(app)
