import pika, sys, os, json
import psycopg2
import logging
from logging.config import dictConfig
from config import log_config

conn = psycopg2.connect(
    host="172.28.32.1",
    port=5432,
    user="postgres",
    password="Aranet1505.",
    database="PlayScore_ASA_db"
)

dictConfig(log_config)
logger = logging.getLogger('foo-logger')

def callback(ch, method, properties, body):
    try:
        body = json.loads(body)
        rating_json = body

        with conn.cursor() as cur:

            cur.execute("SELECT * FROM tb_user WHERE user_id = %s;", (rating_json['user_id'],))
            user_exists = cur.fetchone()

            cur.execute("SELECT * FROM tb_game WHERE game_id = %s;", (rating_json['game_id'],))
            game_exists = cur.fetchone()

            if user_exists and game_exists:

                cur.execute("INSERT INTO tb_rating (user_id, game_id, score) VALUES (%s, %s, %s);",
                            (rating_json['user_id'], rating_json['game_id'], rating_json['score']))
                conn.commit()

                logger.info(f"Rating inserted successfully")
            else:
                logger.error("Failed to insert rating")
    except:
        logger.error(f"Request formated wrong: {rating_json}")

 
def consumer(queuename):

    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost',
                                       5672,
                                       '/',
                                       credentials)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()

    channel.queue_declare(queue=queuename)

    channel.basic_consume(queue=queuename, on_message_callback=callback, auto_ack=True)

    channel.start_consuming()


if __name__ == '__main__':
    queuename = 'rating_post'
    try:
        consumer(queuename=queuename)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)