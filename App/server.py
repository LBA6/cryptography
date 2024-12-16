from flask import Flask, request, jsonify
from waitress import serve

app = Flask(__name__)
users = {}
messages = {}
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    users.update({data['username']:(data['prime_nb'], data['gen'], data['pub_key'])})
    return jsonify({"message":"User "+data['username']+" registered succesfully."}), 200

@app.route('/get_users', methods=['POST'])
def get_users():
    list_of_users = str([x for x in users.keys()])
    return jsonify({"users":list_of_users}), 200

@app.route('/get_user_data', methods=['POST'])
def get_user_data():
    user = request.json['user']
    return jsonify({"prime_nb":users.get(user)[0], "gen":users.get(user)[1], "pub_key":users.get(user)[2]}), 200

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    dest = data['dest']
    new_message = (data['sender'], data['public_key'], data['message'])

    if messages.get(dest):
        tmp = messages.get(dest)
        tmp.append(new_message)
        messages.update({dest: tmp})
    else:
        messages.update({dest: [new_message]})
    
    return jsonify({"message":"Message for "+dest+" send."}), 200

@app.route('/read_messages', methods=['POST'])
def read_message():
    username = request.json['username']
    return jsonify({"messages":messages.get(username)}), 200

if __name__ == '__main__':
    app.run()

serve(app, listen='127.0.0.1:5000')