import copy
import json

class Game:
  default_width = 3
  default_players = ('X', 'O')

  def __init__(self, width=None, players=None, moves=None):
    self.width = Game.default_width if width is None else width
    self.players = Game.default_players if players is None else players
    self.moves = [] if moves is None else moves

  def reset(self):
    self.moves = []

  def add_move(self, big_row, big_col, small_row, small_col):
    self.moves.append((big_row, big_col, small_row, small_col))

  def get_whose_move(self, move_num):
    return self.players[(move_num) % len(self.players)]
  
  def get_full_data(self):

    big_detailed_board = self.get_big_detailed_board()
    big_winner = self.get_big_winner(big_detailed_board)

    return {
      "board": big_detailed_board,
      "current_player": self.get_current_player(),
      "big_winner": big_winner
    }

  def get_current_player(self):
    current_move = len(self.moves)
    return self.get_whose_move(current_move)

  def get_small_empty_board(self):
    return [ [None]*self.width for i in range(self.width)]

  def get_big_empty_board(self):
    empty_board = []
    for i in range(self.width):
      empty_board.append([])
      for j in range(self.width):
        empty_board[i].append(self.get_small_empty_board())
    return empty_board

  def get_small_detailed_board(self, board, i, j):
    small_detailed_board = []
    for k in range(self.width):
      small_detailed_board.append([])
      for l in range(self.width):
        small_detailed_board[k].append({
          "player": board[i][j][k][l],
          "move_is_legal": self.is_move_legal(board, (i,j,k,l))
        })
    return small_detailed_board

  def is_move_legal(self, board, move):
    if(len(self.moves)==0):
      return True
    if(board[move[0]][move[1]][move[2]][move[3]] != None):
      return False
    last_move = self.moves[-1]
    in_target_big_square = (last_move[2], last_move[3]) == (move[0], move[1])
    return in_target_big_square

  def get_big_winner(self, big_detailed_board):
    meta_board = []
    for i in range(self.width):
      meta_board.append([])
      for j in range(self.width):
        meta_board[i].append(big_detailed_board[i][j]['winner'])
    return self.get_board_winner(meta_board)

  def get_big_populated_board(self):
    board = self.get_big_empty_board()
    for move_num, move in enumerate(self.moves):
      player = self.get_whose_move(move_num)
      big_row = move[0]
      big_col = move[1]
      small_row = move[2]
      small_col = move[3]
      board[big_row][big_col][small_row][small_col] = player
    return board

  def last_move_won_board(self, big_detailed_board):
    if len(self.moves) < 1:
      return False
    last_move = self.moves[-1]
    small_board = big_detailed_board[last_move[0]][last_move[1]]
    return small_board['winner']

  def target_board_illegal(self, big_detailed_board):
    if len(self.moves) < 1:
      return False
    last_move = self.moves[-1]
    small_board = big_detailed_board[last_move[2]][last_move[3]]
    return small_board['winner']

  def get_big_detailed_board(self):
    big_populated_board = self.get_big_populated_board()
    big_detailed_board = []
    for i in range(self.width):
      big_detailed_board.append([])
      for j in range(self.width):

        small_detailed_board = self.get_small_detailed_board(big_populated_board, i,j)
        small_populated_board = big_populated_board[i][j]
        winner = self.get_board_winner(small_populated_board)

        big_detailed_board[i].append({
          "winner": winner,
          "small_board": small_detailed_board
        })

    # if last person just won or sent you to already captured small board
    if (self.last_move_won_board(big_detailed_board) or self.target_board_illegal(big_detailed_board)):
      for i in range(self.width):
        for j in range(self.width):
          small_board = big_detailed_board[i][j]['small_board']
          for k in range(self.width):
            for l in range(self.width):
              small_square = small_board[k][l]
              if not small_square['player']:
                small_square["move_is_legal"] = True


    # eliminate captured boards
    for i in range(self.width):
      for j in range(self.width):
        big_square = big_detailed_board[i][j]
        small_board = big_square['small_board']
        winner = big_square['winner']
        if winner:
          for k in range(self.width):
            for l in range(self.width):
              small_square = small_board[k][l]
              small_square["move_is_legal"] = False

    big_winner = self.get_big_winner(big_detailed_board)
    if big_winner:
      # eliminate all squares
      for i in range(self.width):
        for j in range(self.width):
          big_square = big_detailed_board[i][j]
          small_board = big_square['small_board']
          for k in range(self.width):
            for l in range(self.width):
              small_square = small_board[k][l]
              small_square["move_is_legal"] = False

    return big_detailed_board

  def get_board_winner(self, board):
    all_sequences = self.get_all_sequences(board)

    for sequence in all_sequences:
      sequence_winner = self.get_sequence_winner(sequence)
      if sequence_winner:
        return sequence_winner

    return None

  def get_all_sequences(self, board):
    all_sequences = []
    # rows
    for row in board:
      all_sequences.append(row)
    # cols
    for i in range(self.width):
      col = []
      for j in range(self.width):
        col.append(board[j][i])
      all_sequences.append(col)
    # diags
    down_slope = []
    up_slope = []
    for i in range(self.width):
      down_slope.append(board[i][i])
      up_slope.append(board[i][self.width - 1 - i])
    all_sequences.append(down_slope)
    all_sequences.append(up_slope)

    return all_sequences


  def get_sequence_winner(self, sequence):
    s = set(sequence)
    if len(s) > 1:
      return False
    elif list(s)[0] != None:
      return list(s)[0]
