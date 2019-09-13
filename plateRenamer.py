import requests
import base64
import json
import os

# The script uses openALPR's OCR to read licence plates, iterates through a directory and renaming each image to the plate number. 
# NOTE: Only one licence plate should be present in each image.  

# Change the following to the correct image path:
imagePath = "images/"
listing = os.listdir(imagePath)
SECRET_KEY = 'sk_DEMODEMODEMODEMODEMODEMO'

for image in listing:
    with open(imagePath + image, 'rb') as image_file:   
        img_base64 = base64.b64encode(image_file.read())
    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=eu&secret_key=%s' % (SECRET_KEY)
    
    try:
        r = requests.post(url, data = img_base64)
        result_json = r.json()

        # The resulting plate number
        plate_id = result_json["results"][0]["plate"]

        # Renames the file to the plate number
        dst=plate_id + ".jpg"
        src = imagePath + image 
        dst = imagePath + dst 
        os.rename(src, dst) 

        # Prints the new filename
        print("Image renamed to:", plate_id + ".jpg")
    except:
        pass