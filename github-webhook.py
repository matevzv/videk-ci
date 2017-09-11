import os
import sys
import hmac
import hashlib
import subprocess
from flask import Flask, request, jsonify

github_token = sys.argv[1]

users = ["matevzv", "avian2", "sensorlab"]

app = Flask(__name__)

def verify_hmac_hash(data, signature):
    github_secret = bytes(os.environ['SECRET_TOKEN'], 'UTF-8')
    mac = hmac.new(github_secret, msg=data, digestmod=hashlib.sha1)
    return hmac.compare_digest('sha1=' + mac.hexdigest(), signature)

@app.route('/pyload', methods=['POST'])
def webhook():
    signature = request.headers.get('X-Hub-Signature')
    if signature == None:
        return jsonify({'msg': 'missing hash'})

    req = request.data
    if verify_hmac_hash(req, signature):
        data = request.get_json()

        if data['sender']['login'] in users:
            event = request.headers.get('X-GitHub-Event')
            if event == 'ping':
                return jsonify({'msg': 'OK'})
            else
                tag_name = data['release']['tag_name']
                upload_url = data['release']['upload_url'].replace("{?name,label}", "")
                repository_name = data['repository']['name']
                repository_url = data['repository']['clone_url']
                subprocess.Popen(["./releasebuilder", tag_name, upload_url, repository_name, repository_url, github_token])
                return jsonify({'msg': 'OK'})
        else:
            return jsonify({'msg': 'Invalid user!'})
    else:
        return jsonify({'msg': 'invalid hash'})

if __name__ == '__main__':
    app.debug = True
    app.run(host="localhost", port=8000)
