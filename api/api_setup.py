from flask import Flask
import os

api_setup = Flask(__name__)
api_setup.secret_key = os.urandom(32)
api_setup.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
