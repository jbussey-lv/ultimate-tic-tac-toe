from flask import Flask, render_template, request, redirect
from models.game import Game 
from flask_socketio import SocketIO, emit, send, join_room
from simple_websocket.ws import Server as WS
import time 
import random
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

game = Game()

games = {}

def get_new_game_key():
    key_length = 5
    letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    game_key = ''.join(random.choice(letters) for i in range(key_length))
    return game_key

def get_game_link(game_key, player):
    return "/games/" + game_key + "/" + player

def extract_game_key(referrer):
    sub1 = "games/"
    sub2 = "/"
    idx1 = referrer.find(sub1)
    end = referrer[idx1 + len(sub1):]
    idx2 = referrer.find(sub2)
    return end[0: idx2]

@socketio.event
def connect():
    game_key = extract_game_key(request.referrer)
    join_room(game_key)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/games', methods=['POST'])
def create_new_game():
    game_key = get_new_game_key()
    player = Game.players[0]
    game_link = get_game_link(game_key, player)
    games[game_key] = Game()
    return redirect(game_link)

@app.route('/games/<string:game_key>/<string:this_player>')
def get_game(game_key, this_player):
    if(game_key not in games):
        return redirect('/')
    
    game = games[game_key]
    board = game.get_big_detailed_board()
    current_player = game.get_current_player()
    return render_template('game.html', game_key=game_key, board=board, this_player=this_player, current_player=current_player)

@app.route('/games', methods=['GET'])
def join_game():
    game_key = request.args.get('game_key')
    player = Game.players[1]
    game_link = get_game_link(game_key, player)
    return redirect(game_link)

@app.route('/games/<string:game_key>/reset', methods=['POST'])
def reset_game(game_key):
    if(game_key not in games):
        return redirect('/')
    
    game = games[game_key]
    game.reset()

    socketio.emit('message', 'refresh', room=game_key)

    return redirect(request.referrer)

@app.route('/games/<string:game_key>/moves', methods=['POST'])
def moves(game_key):

    if(game_key not in games):
        return redirect('/')
    
    game = games[game_key]
    big_row_index = int(request.form.get('big_row_index'))
    big_col_index = int(request.form.get('big_col_index'))
    small_row_index = int(request.form.get('small_row_index'))
    small_col_index = int(request.form.get('small_col_index'))
    game.add_move(big_row_index, big_col_index, small_row_index, small_col_index)

    socketio.emit('message', 'refresh', room=game_key)

    return redirect(request.referrer)

 
# main driver function
if __name__ == '__main__':
    socketio.run(app)