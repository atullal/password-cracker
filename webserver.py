from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
import server

def start_server():
    server.create_dictionaries()
    server.start_server_node_thread(5004)

start_server()

app = Flask(__name__)
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
    email = data['email']
    password_hash = data['hash']
    clients = data["clients"]
    
    print("Sending " + password_hash)
    
    return server.decrypt_md5(password_hash, clients)