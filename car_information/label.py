import os
from car_information_service import get_data_from_vegvesenet, \
    identify_license_plate
import time
import json
import sys


def get_license_plates_from_images(input_directory):
    data = []
    images = os.listdir(input_directory)

    for image in images:
        print("Identifying plate from image " + image)
        car = {}
        car["image"] = image
        license_plate = identify_license_plate(input_directory, image)
        if license_plate:
            car["registreringsnummer"] = license_plate
            print("Identified license plate " + license_plate)
        else:
            car["registreringsnummer"] = None
            print("Could not identify license plate")
        data.append(car)

    return data


def fetch_data(cars):
    for car in cars:
        license_number = car["registreringsnummer"]
        if license_number:
            print("Fetching data of license number: " + license_number)
            has_fetched = False
            try:
                data = get_data_from_vegvesenet(license_number)
                has_fetched = True
            finally:
                if has_fetched:
                    car["data"] = data
                    print("Fetch ok")
                    print(json.dumps(data))
                else:
                    print("Could not fetch data of: " + license_number)
    return cars


def safe_directory(directory):
    os.makedirs(directory, exist_ok=True)


def move_image(input_directory, output_directory):
    os.rename(input_directory, output_directory)


if __name__ == "__main__":
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    try:
        output_directory_format = sys.argv[3]
    except:
        output_directory_format = None

    car_data = get_license_plates_from_images(input_directory)
    car_data = fetch_data(car_data)

    for car in car_data:
        if car["registreringsnummer"]:
            data = car["data"]

            destination = output_directory
            if output_directory_format == "-C":
                destination += "/" + data["farge"].lower()
            elif output_directory_format == "-B":
                destination += "/" + data["merke"].lower().replace(" ", "_")
            elif output_directory_format == "-M":
                destination += "/" + data["modell"].lower().replace(" ", "_")
            destination += "/"

            safe_directory(destination)
            image = car["image"]
            move_image(input_directory + image, destination + image)
