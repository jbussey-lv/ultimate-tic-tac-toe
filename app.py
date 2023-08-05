from flask import Flask, render_template, request, redirect
from models.game import add_move, get_big_detailed_board, reset_game, get_current_player
 
app = Flask(__name__)
 
@app.route('/')
def game():
    board = get_big_detailed_board()
    current_player = get_current_player()
    return render_template('game.html', board=board, current_player=current_player)

@app.route('/moves', methods=['POST'])
def moves():
    big_row_index = int(request.form.get('big_row_index'))
    big_col_index = int(request.form.get('big_col_index'))
    small_row_index = int(request.form.get('small_row_index'))
    small_col_index = int(request.form.get('small_col_index'))
    add_move(big_row_index, big_col_index, small_row_index, small_col_index)
    return redirect("/")

@app.route('/reset', methods=['POST'])
def reset():
    reset_game()
    return redirect("/")
 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug = True)