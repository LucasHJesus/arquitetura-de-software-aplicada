# CLIENT [ALUNO] >:(

from models import Aluno, session
import pika, sys, os, json


def callback(ch, method, properties, body):
    try:
        body = json.loads(body)
        aluno_json = body

        aluno = Aluno(
            Nome        = aluno_json['nome'],
            Email       = aluno_json['email'],
            CPF         = aluno_json['cpf'],
            Endereco    = aluno_json['endereco'],
            Numero      = aluno_json['numero'],
            Complemento = aluno_json['complemento'],
            Cidade      = aluno_json['cidade'],
            Estado      = aluno_json['estado']
        )
        session.add(aluno)
        session.commit()
        print(f"funcionou {body}")

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
    queuename = 'alunoinsert'
    try:
        consumer(queuename=queuename)
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)