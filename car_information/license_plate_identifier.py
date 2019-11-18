import requests
import base64
import json
import os

# The script uses openALPR's OCR to read licence plates, iterates through
# a directory and renaming each image to the plate number.
# NOTE: Only one licence plate should be present in each image.

# Change the following to the correct image path:
IMAGE_PATH = "images/"
SECRET_KEY = 'sk_DEMODEMODEMODEMODEMODEMO'
OPEN_ALPR_ENDPOINT = 'https://api.openalpr.com/v2/recognize_bytes' \
    + '?recognize_vehicle=1&country=eu&secret_key=%s' % (SECRET_KEY)


def identify_license_plate(path, image):
    with open(path + image, 'rb') as file:
        img_base64 = base64.b64encode(file.read())

    try:
        r = requests.post(OPEN_ALPR_ENDPOINT, data=img_base64)
        result_json = r.json()

        return result_json["results"][0]["plate"]
    except:
        return None


def rename_file(path, file, new_name):
    file_extension = file.split(".")[1]
    new_file = new_name + "." + file_extension
    new_path = path + new_file
    os.rename(path + file, new_path)
    return new_file


images = os.listdir(IMAGE_PATH)
for image in images:
    try:
        license_plate = identify_license_plate(IMAGE_PATH, image)
        filename = rename_file(IMAGE_PATH, image, license_plate)
        print("Renamed " + image + " to " + filename)
    except:
        print("Could not find a license plate in image " + image)
