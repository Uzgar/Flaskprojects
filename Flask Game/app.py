# app.py
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Store player positions and colors
players = {}

def generate_random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    random_color = generate_random_color()
    players[request.sid] = {'x': 0, 'y': 0, 'color': random_color}
    print(f"User connected: {request.sid}")
    update_players()

@socketio.on('disconnect')
def handle_disconnect():
    print(f"User disconnected: {request.sid}")
    # Remove the player on disconnect
    if request.sid in players:
        del players[request.sid]
    # Broadcast updated player list
    update_players()

@socketio.on('move')
def handle_move(data):
    players[request.sid] = {'x': data['x'], 'y': data['y'], 'color': players[request.sid]['color']}
    update_players()

def update_players():
    socketio.emit('update_players', players, namespace='/')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=4710, debug=True)

