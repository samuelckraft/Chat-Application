from web_socket_server import WebSocketServer, socketio, app
from flask import render_template, request, json

app = WebSocketServer().create_app()
message_storage = {}


@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('message')
def handle_message(data):
    try:
        data = json.loads(data)
        user = data['user']
        message = data['message']
        print(f'Received message from {user}: {message}')
        
        if user not in message_storage:
            message_storage[user] = []
        message_storage[user].append(message)
        
        socketio.emit('message', data)
    except (KeyError) as e:
        print(f'Error processing message: {e}')

@app.route('/')
def index():
    return render_template('WebSocketClient.html')

@app.route('/get_all_messages', methods=['GET'])
def get_all_messages():
    user = request.args.get('user')
    if user in message_storage:
        print({'messages': message_storage[user]})
    else:
        return {'messages': []}



if __name__ == '__main__':
    socketio.run(app)