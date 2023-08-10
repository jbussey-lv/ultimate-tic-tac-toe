from flask import Flask, render_template, request, redirect
from models.game import Game 
from flask_socketio import SocketIO, emit, send, join_room
from simple_websocket.ws import Server as WS
import time
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)

game = Game()

@socketio.event
def connect():
    join_room('abc')

@socketio.event
def my_custom_event(arg1):
    send(arg1, room='abc')

@app.route('/becho')
def becho():
    response = render_template('becho.html')
    return response


 
@app.route('/')
def home():
    board = game.get_big_detailed_board()
    current_player = game.get_current_player()
    return render_template('game.html', board=board, current_player=current_player)

@app.route('/moves', methods=['POST'])
def moves():
    big_row_index = int(request.form.get('big_row_index'))
    big_col_index = int(request.form.get('big_col_index'))
    small_row_index = int(request.form.get('small_row_index'))
    small_col_index = int(request.form.get('small_col_index'))
    game.add_move(big_row_index, big_col_index, small_row_index, small_col_index)
    return redirect("/")

@app.route('/reset', methods=['POST'])
def reset():
    game.reset_game()
    return redirect("/")
 
# main driver function
if __name__ == '__main__':
    socketio.run(app)