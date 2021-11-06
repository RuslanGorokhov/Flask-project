import os

import requests
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from flask import Blueprint
from dotenv import load_dotenv
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

parser_bp = Blueprint('parser', __name__, url_prefix='/parser')
excel_validation_bp = Blueprint('validation', __name__, url_prefix='/validation')

app.register_blueprint(parser_bp)
app.register_blueprint(excel_validation_bp)

Upload_file = 'C:\\Users\\Кирилл\\projects\\Папка для файлов из бота'
Allowed_extensions = set(['xlsx'])
app.config['Upload_file'] = Upload_file

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in Allowed_extensions


def report_messages(chat_id, text):
    method = "sendMessage"
    code = os.getenv("API_KEY")
    url = f"https://api.telegram.org/bot{code}/{method}"
    data_address = {"chat_id": chat_id, "text": text}
    requests.post(url, data_address=data_address)


def s_messege(chat_id, text='Результат получен'):
    method = "sendMessage"
    code = os.getenv("API_KEY")
    url = f"https://api.telegram.org/bot{code}/{method}"
    answer = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=answer)
    return r.json()


@app.route("/", methods=["POST"])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['Upload_file'], filename))
            return {"ok": True}


if __name__ == "__main__":
    app.run()
    load_dotenv()
