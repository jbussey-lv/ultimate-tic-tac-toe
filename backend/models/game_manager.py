import random
from models.game import Game

import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

games_collection = mongo_client["ultic"]["games"]
# mydict = { "name": "John", "address": "Highway 37" }

# x = games.insert_one(mydict)

class GameManager:

  @staticmethod
  def create_game():
    game = Game()
    key = GameManager.get_new_game_key()
    GameManager.create_game_record(key, game)
    return key, game
  
  @staticmethod
  def get_game_dict(game):
    return game.__dict__
  
  @staticmethod
  def create_game_record(key, game):
    game_dict = GameManager.get_game_dict(game)
    games_collection.insert_one({"key": key, "game": game_dict})

  @staticmethod
  def retrieve_game_record(key):
    game_record = games_collection.find_one({"key": key})
    game_dict = game_record["game"]
    game = Game(**game_dict)
    return game

  @staticmethod
  def update_game_record(key, game):
    game_dict = GameManager.get_game_dict(game)
    games_collection.update_one({"key": key}, {"$set": {"game": game_dict}})


  @staticmethod
  def get_new_game_key():
    key_length = 5
    letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    game_key = ''.join(random.choice(letters) for i in range(key_length))
    return game_key
  
  @staticmethod
  def retrieve_game(key):
    game = GameManager.retrieve_game_record(key)
    return game
  
  @staticmethod
  def save_game(key, game):
    GameManager.update_game_record(key, game)