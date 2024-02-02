import base64
import threading
import time
from flask import Flask, render_template, Response
from flask_socketio import SocketIO
import mss

app = Flask(__name__)
socketio = SocketIO(app)

shared_screen_data = None

def generate():
    global shared_screen_data
    while True:
        if shared_screen_data:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + shared_screen_data + b'\r\n\r\n')
            time.sleep(0.1)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('share_screen')
def handle_share_screen(data):
    print(f'Screen shared by {data["username"]}')
    socketio.emit('screen_shared', data, broadcast=True)

def capture_screen():
    global shared_screen_data
    with mss.mss() as sct:
        while True:
            # Capture the screen
            screenshot = sct.shot(output=None)

            # Convert the image to base64 for streaming
            with open(screenshot, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                shared_screen_data = encoded_string

            time.sleep(0.1)

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    capture_thread = threading.Thread(target=capture_screen)
    capture_thread.start()
    socketio.run(app, debug=True)
