from pydantic import BaseModel

class User(BaseModel):
    user_id  : int
    username : str
    email    : str
    password : str

class Game(BaseModel):
    game_id     : int
    title       : str
    developer   : str
    total_score : float
    description : str
    category    : str
    imageURL    : str 

class ShortGame(BaseModel):
    title       : str
    total_score : float
    imageURL    : str 

class Rating(BaseModel):
    user_id : int
    game_id : int
    score   : float