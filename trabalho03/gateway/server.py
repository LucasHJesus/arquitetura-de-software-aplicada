from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from classes import User, Game, Rating, ShortGame
import psycopg2
import pika
import json

app = FastAPI()

conn = psycopg2.connect(
    host="172.28.32.1",
    port=5432,
    user="postgres",
    password="Aranet1505.",
    database="PlayScore_ASA_db"
)

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost',
                                   5672,
                                   '/',
                                   credentials)


# ROOT-----------------------------------------------------------------------------------------#


@app.get("/")
async def root():
    return {
        "status": "SUCESS",
        "data": "NO DATA"
    }


# USER ENDPOINTS-------------------------------------------------------------------------------#


@app.get("/user_by_username/{username}")
async def get_user(username: str):
    try:
        with conn.cursor() as cur:

            cur.execute("SELECT * FROM tb_user WHERE username = %s;", (username,))
            user_data = cur.fetchone()

            if user_data:
                user_dict = {
                    "user_id"  : user_data[0],
                    "username" : user_data[1],
                    "email"    : user_data[2],
                    "password" : user_data[3]
                }

                return JSONResponse(content=jsonable_encoder(user_dict))
            else:
                raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        print(f"Error: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/user")
async def post_user(user_data: User):
    try:
        user_json = {
        "username" : user_data.username,
        "email"    : user_data.email,
        "password" : user_data.password,
        }
        queuename = 'user_post'
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=queuename)
        channel.basic_publish(exchange='', routing_key=queuename, body=json.dumps(user_json), 
                              properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        channel.close()

    except Exception as e:
        print(f"Error: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")


@app.put("/user")
async def put_user(user_data: User):
    try:
        user_json = {
        "user_id"  : user_data.user_id,
        "username" : user_data.username,
        "email"    : user_data.email,
        "password" : user_data.password,
        }
        queuename = 'user_put'
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=queuename)
        channel.basic_publish(exchange='', routing_key=queuename, body=json.dumps(user_json), 
                              properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        channel.close()

    except Exception as e:
        print(f"Error: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")


# GAME ENDPOINTS-------------------------------------------------------------------------------#


@app.get("/games")
async def get_all_games():
    try:
        with conn.cursor() as cur:

            cur.execute("SELECT title, total_score, imageURL FROM tb_game;")
            games_data = cur.fetchall()

            games_list = []
            for game_data in games_data:
                game = ShortGame(title=game_data[0], total_score=game_data[1], imageURL=game_data[2])
                games_list.append(game)

            return JSONResponse(content=jsonable_encoder(games_list))
    except Exception as e:
        print(f"Error: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/games/{category}")
async def get_games_by_category(category: str):
    try:
        with conn.cursor() as cur:

            cur.execute("SELECT title, total_score, imageURL FROM tb_game WHERE category = %s;", (category,))
            games_data = cur.fetchall()

            games_list = []
            for game_data in games_data:
                game = ShortGame(title=game_data[0], total_score=game_data[1], imageURL=game_data[2])
                games_list.append(game)

            return JSONResponse(content=jsonable_encoder(games_list))
    except Exception as e:
        print(f"Error: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/game_by_title/{title}")
async def get_game_by_title(title: str):
    try:
        with conn.cursor() as cur:

            cur.execute("SELECT * FROM tb_game WHERE title = %s;", (title,))
            game_data = cur.fetchone()

            if game_data:
                game = Game(
                    game_id=game_data[0],
                    title=game_data[1],
                    developer=game_data[2],
                    total_score=game_data[3],
                    description=game_data[4],
                    category=game_data[5],
                    imageURL=game_data[6]
                )

                return JSONResponse(content=jsonable_encoder(game))
            else:
                raise HTTPException(status_code=404, detail="Game not found")
    except Exception as e:
        print(f"Error: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")


# RATING ENDPOINT-------------------------------------------------------------------------------#


@app.post("/rating")
async def add_rating(rating: Rating):
    try:
        rating_json = {
        "user_id" : rating.user_id,
        "game_id" : rating.game_id,
        "score"   : rating.score,
        }
        queuename = 'rating_post'
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=queuename)
        channel.basic_publish(exchange='', routing_key=queuename, body=json.dumps(rating_json), 
                              properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        channel.close()
    except Exception as e:
        print(f"Error: {e}")
        return HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    

@app.put("/rating")
async def put_rating(rating: Rating):
    try:
        rating_json = {
        "user_id" : rating.user_id,
        "game_id" : rating.game_id,
        "score"   : rating.score
        }
        queuename = 'rating_put'
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(queue=queuename)
        channel.basic_publish(exchange='', routing_key=queuename, body=json.dumps(rating_json), 
                              properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        channel.close()
    except Exception as e:
        print(f"Error: {e}")
        return HTTPException(status_code=500, detail="Internal Server Error")