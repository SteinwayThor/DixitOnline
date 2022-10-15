from flask import Flask, request, send_from_directory
from flask_socketio import SocketIO, emit
from stablediffusion_dixit.game_logic.player import Player


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

@app.route("/images/<path:path>")
def serve_image(path):
    return send_from_directory("images", path)

@app.route("/animations/<path:path>")
def serve_anim(path):
    return send_from_directory("animations", path)

@socketio.on("join_game")
def join_game(data):
    player = Player(request.sid,data['name'])
    game_state.players.append(player)

@socketio.on("enter_prompt")
def enter_prompt(data):
    prompt_text = data["prompt"]
    game_state.receive_prompt(request.sid,prompt_text)
    

@socketio.on("start_game")
def start_game():
    game_state.active_player_write_prompt()

@socketio.on("active_player_proceed")
def proceed():
    game_state.active_player_proceed(request.sid)

@socketio.on("vote")
def vote(data):
    game_state.recieve_vote(request.sid,data['vote'])

@socketio.on("disconnect")
def disconnect(data):
    dc_player = game_state.get_player(request.sid)
    game_state.players.remove(dc_player)
    game_state.reset()


if __name__ == "__main__":
    socketio.run(app)
