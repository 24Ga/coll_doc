import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC6dd1bb5d6fc2c849b5539a38a3950a42'
    TWILIO_SYNC_SERVICE_SID = 'IS6583cba2e2386db640065a1ed1a51a6a'
    TWILIO_API_KEY = 'SK4bcc3ba11c3d3d425dff6e8657076fa2'
    TWILIO_API_SECRET = 'IC7UQOGgoY8bpQ82oAPOTcPcECoPGxqu'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# A function to download text and store it in text file
@app.route('/', methods=['POST'])
def download_text():
    text_from_notepad = request.form['text']
    with open('workfile.txt', 'w') as f:
        f.write(text_from_notepad)

    path_to_store_txt = "workfile.txt"

    return send_file(path_to_store_txt, as_attachment=True)


if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
