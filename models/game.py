import copy

width = 3

players = ('X', 'O')

moves = []

def reset_game():
  global moves
  moves = []

def add_move(big_row, big_col, small_row, small_col):
  global moves
  moves.append((big_row, big_col, small_row, small_col))

def get_whose_move(move_num):
  global players
  return players[(move_num) % len(players)]

def get_current_player():
  global moves
  global players
  current_move = len(moves)
  return get_whose_move(current_move)

def get_small_empty_board(width):
  return [ [None]*width for i in range(width)]

def get_big_empty_board(width):
  empty_board = []
  for i in range(width):
    empty_board.append([])
    for j in range(width):
      empty_board[i].append(get_small_empty_board(width))
  return empty_board

def get_small_detailed_board(board, i, j):
  small_detailed_board = []
  for k in range(width):
    small_detailed_board.append([])
    for l in range(width):
      small_detailed_board[k].append({
        "player": board[i][j][k][l],
        "move_is_legal": is_move_legal(board, (i,j,k,l))
      })
  return small_detailed_board

def is_move_legal(board, move):
  global moves
  if(len(moves)==0):
    return True
  if(board[move[0]][move[1]][move[2]][move[3]] != None):
    return False
  last_move = moves[-1]
  in_target_big_square = (last_move[2], last_move[3]) == (move[0], move[1])
  return in_target_big_square

def get_big_winner(big_detailed_board):
  meta_board = []
  for i in range(width):
    meta_board.append([])
    for j in range(width):
      meta_board[i].append(big_detailed_board[i][j]['winner'])
  return get_board_winner(meta_board)

def get_big_populated_board():
  global width, moves, players
  board = get_big_empty_board(width)
  for move_num, move in enumerate(moves):
    player = get_whose_move(move_num)
    big_row = move[0]
    big_col = move[1]
    small_row = move[2]
    small_col = move[3]
    board[big_row][big_col][small_row][small_col] = player
  return board

def last_move_won_board(big_detailed_board):
  global moves
  if len(moves) < 1:
    return False
  last_move = moves[-1]
  small_board = big_detailed_board[last_move[0]][last_move[1]]
  return small_board['winner']

def target_board_illegal(big_detailed_board):
  global moves
  if len(moves) < 1:
    return False
  last_move = moves[-1]
  small_board = big_detailed_board[last_move[2]][last_move[3]]
  return small_board['winner']

def get_big_detailed_board():
  big_populated_board = get_big_populated_board()
  big_detailed_board = []
  for i in range(width):
    big_detailed_board.append([])
    for j in range(width):

      small_detailed_board = get_small_detailed_board(big_populated_board, i,j)
      small_populated_board = big_populated_board[i][j]
      winner = get_board_winner(small_populated_board)

      big_detailed_board[i].append({
        "winner": winner,
        "small_board": small_detailed_board
      })

  # if last person just won or sent you to already captured small board
  if (last_move_won_board(big_detailed_board) or target_board_illegal(big_detailed_board)):
    for i in range(width):
      for j in range(width):
        small_board = big_detailed_board[i][j]['small_board']
        for k in range(width):
          for l in range(width):
            small_square = small_board[k][l]
            if not small_square['player']:
              small_square["move_is_legal"] = True


  # eliminate captured boards
  for i in range(width):
    for j in range(width):
      big_square = big_detailed_board[i][j]
      small_board = big_square['small_board']
      winner = big_square['winner']
      if winner:
        for k in range(width):
          for l in range(width):
            small_square = small_board[k][l]
            small_square["move_is_legal"] = False

  big_winner = get_big_winner(big_detailed_board)
  if big_winner:
    # eliminate all squares
    for i in range(width):
      for j in range(width):
        big_square = big_detailed_board[i][j]
        small_board = big_square['small_board']
        for k in range(width):
          for l in range(width):
            small_square = small_board[k][l]
            small_square["move_is_legal"] = False

  return {
    "big_winner": big_winner,
    "board": big_detailed_board
  }

def get_board_winner(board):
  all_sequences = get_all_sequences(board)

  for sequence in all_sequences:
    sequence_winner = get_sequence_winner(sequence)
    if sequence_winner:
      return sequence_winner

  return None

def get_all_sequences(board):
  width = len(board)
  all_sequences = []
  # rows
  for row in board:
    all_sequences.append(row)
  # cols
  for i in range(width):
    col = []
    for j in range(width):
      col.append(board[j][i])
    all_sequences.append(col)
  # diags
  down_slope = []
  up_slope = []
  for i in range(width):
    down_slope.append(board[i][i])
    up_slope.append(board[i][width - 1 - i])
  all_sequences.append(down_slope)
  all_sequences.append(up_slope)

  return all_sequences



def get_sequence_winner(sequence):
  s = set(sequence)
  if len(s) > 1:
    return False
  elif list(s)[0] != None:
    return list(s)[0]
