# CLIENT [CURSO] >:(

from models import Curso, session
import pika, sys, os, json


def callback(ch, method, properties, body):
    try:
        body = json.loads(body)
        curso_json = body

        curso = Curso(
            Nome                  = curso_json['nome'],
            Professor_idProfessor = curso_json['id_professor']
            
        )
        session.add(curso)
        session.commit()

    except:
        print(f"Request formated wrong: {body}")

 
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
    queuename = 'cursoinsert'
    try:
        consumer(queuename=queuename)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)