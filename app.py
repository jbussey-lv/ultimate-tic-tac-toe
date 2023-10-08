from flask import Flask, render_template, request, redirect
from models.game import Game
from models.game_manager import GameManager 
from flask_socketio import SocketIO, emit, send, join_room
from simple_websocket.ws import Server as WS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app, cors_allowed_origins="*")

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
    game_key = 'ANANM' # extract_game_key(request.referrer)
    join_room(game_key)
    game = GameManager.retrieve_game(game_key)
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


@app.route('/api/games/<string:game_key>', methods=['GET'])
def api_game_data(game_key):
    try:
        game = GameManager.retrieve_game(game_key)
    except:
        return {"error": f'no game found for key {game_key}'}
    
    return game.get_full_data()


@app.route('/games', methods=['GET'])
def join_game():
    key = request.args.get('game_key')
    game = GameManager.retrieve_game(key)
    player = game.players[1]
    game_link = get_game_link(key, player)
    return redirect(game_link)

@app.route('/games/<string:game_key>/reset', methods=['POST'])
def reset_game(game_key):

    try:
        game = GameManager.retrieve_game(game_key)
    except:
        redirect ('/')
    
    GameManager.save_game(game_key, game)

    socketio.emit('game_data', game.get_full_data(), room=game_key)

    return redirect(request.referrer)

@app.route('/games/<string:game_key>/moves', methods=['POST'])
def moves(game_key):
    try:
        game = GameManager.retrieve_game(game_key)
    except:
        redirect ('/')

    big_row_index = int(request.form.get('big_row_index'))
    big_col_index = int(request.form.get('big_col_index'))
    small_row_index = int(request.form.get('small_row_index'))
    small_col_index = int(request.form.get('small_col_index'))
    game.add_move(big_row_index, big_col_index, small_row_index, small_col_index)

    GameManager.save_game(game_key, game)

    socketio.emit('message', 'refresh', room=game_key)

    return redirect(request.referrer)

 
# main driver function
if __name__ == '__main__':
    socketio.run(app)