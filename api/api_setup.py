from flask import Flask
import os

def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

filepath = os.getcwd()

UPLOAD_FOLDER = filepath + '/uploads'
ensure_folder(UPLOAD_FOLDER)

api_setup = Flask(__name__)
api_setup.secret_key = "secret key"
api_setup.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
api_setup.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
