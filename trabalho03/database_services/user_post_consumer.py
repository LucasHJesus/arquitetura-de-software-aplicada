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
        user_json = body
        #print("1")
        with conn.cursor() as cur:
            #print("2")
            cur.execute(
                "INSERT INTO tb_user (username, email, password_key) VALUES (%s, %s, %s) RETURNING *;",
                (user_json['username'], user_json['email'], user_json['password'])
            )
            #print("3")
            conn.commit()
            #print("4")
            updated_data = cur.fetchone()
            #print("5")
            if updated_data:
                #print("6")
                logger.info(f"User with id {updated_data[0]} inserted successfully")
            else:
                #print("7")
                logger.error("Failed to insert user")
    except:
        logger.error(f"Request formated wrong: {user_json}")

 
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
    queuename = 'user_post'
    try:
        consumer(queuename=queuename)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)