from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# List to store drawing data
drawing_data = []

@app.route('/')
def index():
    return render_template('index.html', drawing_data=drawing_data)

@socketio.on('draw')
def handle_draw(data):
    drawing_data.append(data)
    emit('draw', data, broadcast=True)

@socketio.on('connect')
def handle_connect():
    emit('load_drawing', drawing_data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=4780 , debug=True)
