from flask import Flask, render_template, request, redirect
from models.game import Game 
from flask_socketio import SocketIO, emit
from simple_websocket.ws import Server as WS
import time
 
app = Flask(__name__)

socketio = SocketIO(app)

game = Game()

@socketio.on('my event', namespace='/echo')
def my_event(message):
    emit('my response', {'data': 'got it!'})

def echo(ws: WS):
    global message
    old_message = message
    while True:
        new_message = message
        if new_message != old_message:
            old_message = new_message
            ws.send(new_message)

@app.route('/becho')
def becho():
    response = render_template('becho.html')
    return response

@app.route('/message', methods=['POST'])
def message_in():
    global message
    message = request.form.get('message')
    return ""
 
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
 
    # run() method of Flask class runs the application
    # on the local development server.
    socketio.run(app)