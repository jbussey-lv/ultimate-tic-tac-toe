from flask import Flask, render_template, request, redirect
from models.game import Game
from models.game_manager import GameManager 
from flask_socketio import SocketIO, emit, send, join_room
from simple_websocket.ws import Server as WS
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins="*")

def get_game_link(game_key, player):
    return "/games/" + game_key + "/" + player

@socketio.event
def connect():
    game_key = request.args['gameKey']
    join_room(game_key)
    game = GameManager.retrieve_game(game_key)
    socketio.emit('game_data', game.get_full_data(), room=game_key)

@socketio.on('make-move')
def handle_make_move(data):
    coords = tuple(data['coords'])
    game_key = data['gameKey']
    game = GameManager.retrieve_game(game_key)
    game.add_move(coords)
    GameManager.save_game(game_key, game)
    socketio.emit('game_data', game.get_full_data(), room=game_key)

@socketio.on('reset')
def handle_reset(data):
    game_key = data['gameKey']
    game = GameManager.retrieve_game(game_key)
    game.reset()
    GameManager.save_game(game_key, game)
    socketio.emit('game_data', game.get_full_data(), room=game_key)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/games', methods=['POST'])
def create_new_game():
    key, game = GameManager.create_game()
    player = game.players[0]
    game_link = get_game_link(key, player)
    return redirect(game_link)

@app.route('/games/<string:game_key>/<string:this_player>')
def get_game(game_key, this_player):
    try:
        game = GameManager.retrieve_game(game_key)
    except:
        return redirect ('/')
    
    full_data = game.get_full_data()
    
    return render_template('game.html', game_key=game_key, this_player=this_player, **full_data)


@app.route('/games', methods=['GET'])
def join_game():
    key = request.args.get('game_key')
    game = GameManager.retrieve_game(key)
    player = game.players[1]
    game_link = get_game_link(key, player)
    return redirect(game_link)
 
# main driver function
if __name__ == '__main__':
    socketio.run(app)