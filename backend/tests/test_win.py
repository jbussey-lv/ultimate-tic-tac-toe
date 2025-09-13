# tests/test_endpoints/test_calculation_endpoints.py

from models.game import get_board_winner

def test_top_row():
  board = [
    ['x','x','x'],
    [None, None, None],
    [None, None, None]
  ]

  assert get_board_winner(board) == 'x'

def test_no_winner():
  board = [
    ['x','x','o'],
    [None, None, None],
    [None, None, None]
  ]

  assert get_board_winner(board) == None



def test_diagonal():
  board = [
    ['x','o','x'],
    [None, 'x', None],
    [None, None, 'x']
  ]

  assert get_board_winner(board) == 'x'