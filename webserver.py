from flask import Flask, session
from flask import request, jsonify
from flask_cors import CORS
import server
import asyncio
from websockets import serve
import threading
from flask_sock import Sock
import json

def start_server():
    # server.create_dictionaries()
    server.start_server_node_thread(5004)

start_server()
app = Flask(__name__)
sock = Sock(app)
CORS(app)


@app.route("/")
def hello_world():
    return {
        "hello": "world"
    }

@app.route("/get-available-clients")
def available_clients():
    return server.get_available_clients()

# clients = [{"address": "123214", "port": 2145}]
@app.route("/password-cracker", methods = ['POST'])
def password_cracker():
    data = request.get_json()
    # email = data['email']
    password_hash = data['hash']
    clients = data["clients"]
    
    print("Sending " + password_hash)
    
    return server.decrypt_md5(password_hash, clients)

@app.route("/add-client", methods = ['POST'])
def add_client():
    data = request.get_json()
    request_id = data['requestId']
    clients = data["clients"]
    password_hash = data['hash']
    
    return server.add_client(request_id, clients, password_hash)

# @app.route("/password-crack-status/<int:request_id>")
# def password_cracker(request_id):
#     data = request.get_json()
#     return server.add_client(request_id)


@sock.route('/password')
def password_response(sock):
    while True:
        data = json.loads(sock.receive())
        result = server.send_password_response(data["request_id"])
        sock.send(result)

