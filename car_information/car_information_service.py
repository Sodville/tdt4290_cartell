import requests
from bs4 import BeautifulSoup
import base64
import json
import os
from model.Car import Car

SECRET_KEY = 'sk_DEMODEMODEMODEMODEMODEMO'
OPEN_ALPR_ENDPOINT = 'https://api.openalpr.com/v2/recognize_bytes' \
    + '?recognize_vehicle=1&country=eu&secret_key=%s' % (SECRET_KEY)
VEGVESENET_API_ENDPOINT = "https://www.vegvesen.no/ws/no/vegvesen/kjoretoy/" \
    + "kjoretoyoppslag/v1/kjennemerkeoppslag/kjoretoy/"


# NOTE: Only one licence plate should be present in each image.
def identify_license_plate(path, image):
    with open(path + image, 'rb') as file:
        img_base64 = base64.b64encode(file.read())

    try:
        r = requests.post(OPEN_ALPR_ENDPOINT, data=img_base64)
        result_json = r.json()
        print(result_json)

        # If several plates are in the image, the one with the largest square area should be returned
        largest_plate = [0, 0]  # [0] is plate_index [1] is size of that plate
        for i in range (len(result_json.get("results)"))):
            plate_height = result_json.get("results")[i].get("vehicle_region").get("height")
            plate_width = result_json.get("results")[i].get("vehicle_region").get("width")
            plate_size = plate_height*plate_width
            if plate_size > largest_plate[1]:
                largest_plate[0] = i
                largest_plate[1] = plate_size
        return result_json["results"][largest_plate[0]]["plate"]
    except:
        return None


def get_data_from_vegvesenet(license_plate):

    response = requests.get(VEGVESENET_API_ENDPOINT + license_plate).json()

    car = Car()
    car = car.load_data_from_vegvesenet(response)

    return car.get_data()

identify_license_plate()