# CLIENT [PROFESSOR] >:(

from models import Professor, session
import pika, sys, os, json


def callback(ch, method, properties, body):
    try:
        body = json.loads(body)
        professor_json = body

        professor = Professor(
            Nome        = professor_json['nome'],
            Email       = professor_json['email'],
            CPF         = professor_json['cpf'],
            Endereco    = professor_json['endereco'],
            Numero      = professor_json['numero'],
            Complemento = professor_json['complemento'],
            Cidade      = professor_json['cidade'],
            Estado      = professor_json['estado']
        )
        session.add(professor)
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
    queuename = 'professorinsert'
    try:
        consumer(queuename=queuename)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)