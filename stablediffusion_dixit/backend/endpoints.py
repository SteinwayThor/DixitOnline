from flask import Flask, request
from flask_socketio import SocketIO

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


@socketio.on("message")
def join_game(data):
    print(data)


if __name__ == "__main__":
    socketio.run(app)
