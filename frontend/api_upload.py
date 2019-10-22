import os
import urllib.request
import argparse
import fleep

from api_setup import api_setup
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from model_utils import predict, load_model, load_image, get_brands

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(file):
    info = fleep.get(file.read(128))
    return info.extension[0] in ALLOWED_EXTENSIONS

@api_setup.route('/file-upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file: #and allowed_file(file): #TODO: fix allowed_file
        encoded_image = file.read()
        image = load_image(encoded_image)
        pred = predict(model, image, brands)
        resp = jsonify(str(pred))
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(
            {'message': 'Allowed file types are png, jpg, jpeg'})
        resp.status_code = 400
        return resp

def make_argparser():
    parser = argparse.ArgumentParser(description='Predict car brands')
    parser.add_argument('-w', '--weights_path', default='./efficientnetb0_512.hdf5', 
            type=str, help="Path to weights for model")
    parser.add_argument('-b', '--brands_path', default='./brands.txt', 
            type=str, help="Path to brand labels for model")
    return parser

if __name__ == "__main__":
    args = make_argparser().parse_args()

    brands = get_brands(args.brands_path)
    model = load_model(args.weights_path)
    print("Model was loaded succesfully.")

    api_setup.run(host="0.0.0.0")
