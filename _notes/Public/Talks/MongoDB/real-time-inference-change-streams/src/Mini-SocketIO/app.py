from flask import Flask, render_template
from flask_socketio import SocketIO
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.llm_utils import invoke_llm

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable WebSockets

@app.route('/')
def index():
    return render_template('index.html')  # Serve the frontend

# Event listener for messages
@socketio.on('message')
def handle_message(msg):
    print(f"📩 Received message: {msg}")
    socketio.send(f"User message: {msg}")
    server_response = invoke_llm(user_prompt=msg)
    
    # Broadcast message to all connected clients
    socketio.send(f"Server received: {server_response}")

if __name__ == '__main__':
    print("🚀 Starting WebSocket server...")
    socketio.run(app, debug=True, host="0.0.0.0", port=5002)
