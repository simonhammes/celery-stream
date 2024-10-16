# Fix "RuntimeError: Redis requires a monkey patched socket library to work with gevent"
from gevent import monkey

monkey.patch_all()

from flask import Flask, render_template  # noqa
from flask_socketio import SocketIO  # noqa

from tasks import generate_primes  # noqa

app = Flask(__name__)
socketio = SocketIO(app, message_queue='redis://redis:6379')


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('json')
def handle_message(json):
    match json.get('type'):
        case 'generate-primes':
            count = int(json["count"])
            socketio.emit('logs', {'message': f'Received request to generate {count} primes'})
            generate_primes.delay(count)
        case _:
            print(f'Received JSON: {json}')


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 5000
    # TODO: Use logging library
    print(f'Listening on {host}:{port}')
    socketio.run(app, host, port)
