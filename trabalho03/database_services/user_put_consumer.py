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

        with conn.cursor() as cur:
            cur.execute(
                "UPDATE tb_user SET username = %s, email = %s, password_key = %s WHERE user_id = %s;",
                (user_json['username'], user_json["email"], user_json['password'], user_json['user_id'])
            )
            if cur.rowcount > 0:
                conn.commit()
                logger.info(f"User updated successfully")
            else:
                logger.error("Failed to update user")
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
    queuename = 'user_put'
    try:
        consumer(queuename=queuename)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)