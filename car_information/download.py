import os
from car_information_service import get_data_from_vegvesenet, identify_license_plate
import time
import json
import sys


def get_license_plates_from_images(input_directory):
    license_plates = []
    images = os.listdir(input_directory)

    for image in images:
        print("Identifying plate from image " + image)
        license_plate = identify_license_plate(input_directory, image)
        if license_plate:
            license_plates.append(license_plate)
            print("Identified license plate " + license_plate)
        else:
            print("Could not identify license plate")

    return license_plates


def dump_json_to_file(directory, filepath, data):
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, filepath + ".json"), "w") as outfile:
        outfile.write(json.dumps(data))


def fetch_data(license_numbers):
    data = []

    for license_number in license_numbers:
        print("Fetching data of license number: " + license_number)
        has_fetched = False

        try:
            car = get_data_from_vegvesenet(license_number)
            has_fetched = True
        finally:
            if has_fetched:
                data.append(car)
                print("Fetch ok")
                print(json.dumps(car))
            else:
                print("Could not fetch data of: " + license_number)
            time.sleep(1)

    return data

if __name__ == "__main__":
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    try:
        output_directory_format = sys.argv[3]
    except:
        output_directory_format = None

    license_plates = get_license_plates_from_images(input_directory)
    data = fetch_data(license_plates)

    for car in data:
        dump_destination = output_directory
        if output_directory_format == "-C":
            dump_destination += "/" + car["farge"].lower()
        elif output_directory_format == "-B":
            dump_destination += "/" + car["merke"].lower().replace(" ", "_")
        elif output_directory_format == "-M":
            dump_destination += "/" + car["modell"].lower().replace(" ", "_")
        dump_json_to_file(dump_destination, car["registreringsnummer"], car)
