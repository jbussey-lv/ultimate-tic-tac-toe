import random
from models.game import Game

class GameManager:

  games = {}

  @staticmethod
  def create_game():
    game = Game()
    key = GameManager.get_new_game_key()
    GameManager.games[key] = game
    return key, game

  @staticmethod
  def get_new_game_key():
    key_length = 5
    letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    game_key = ''.join(random.choice(letters) for i in range(key_length))
    return game_key
  
  @staticmethod
  def retrieve_game(key):
    return GameManager.games[key]
  
  @staticmethod
  def save_game(key, game):
    GameManager.games[key] = game