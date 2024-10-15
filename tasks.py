import math

from celery import Celery
from flask_socketio import SocketIO
from time import sleep

# TODO: __name__?
app = Celery('tasks', broker='amqp://rabbitmq')
socketio = SocketIO(message_queue='redis://redis:6379')

@app.task
def generate_primes(count: int):
    socketio.emit('logs', {'message': 'Start generating primes...'})

    X = 0
    i = 2
    flag = False

    while(X < count):
        flag = True

        for j in range(2, math.floor(math.sqrt(i)) + 1):
            if (i%j == 0):
                flag = False
                break

        if(flag):
            socketio.emit('logs', {'message': f'Next prime: {i}'})
            X+=1
            sleep(1)

        i+=1

    socketio.emit('logs', {'message': f'Successfully generated {count} primes'})
