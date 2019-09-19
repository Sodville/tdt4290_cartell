import requests
import base64
import json
import os

# The script uses openALPR's OCR to read licence plates, iterates through
# a directory and renaming each image to the plate number.
# NOTE: Only one licence plate should be present in each image.

# Change the following to the correct image path:
IMAGE_PATH = "images/"
images = os.listdir(IMAGE_PATH)
SECRET_KEY = 'sk_DEMODEMODEMODEMODEMODEMO'
OPEN_ALPR_ENDPOINT = 'https://api.openalpr.com/v2/recognize_bytes' \
    + '?recognize_vehicle=1&country=eu&secret_key=%s' % (SECRET_KEY)


for image in images:
    with open(IMAGE_PATH + image, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())

    try:
        r = requests.post(OPEN_ALPR_ENDPOINT, data=img_base64)
        result_json = r.json()

        # The resulting plate number
        plate_id = result_json["results"][0]["plate"]

        # Renames the file to the plate number
        dst = plate_id + ".jpg"
        src = IMAGE_PATH + image
        dst = IMAGE_PATH + dst
        os.rename(src, dst)

        # Prints the new filenameimagePath
        print("Image renamed to:", plate_id + ".jpg")
    except:
        pass
