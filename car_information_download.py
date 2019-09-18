from os import listdir
from os.path import isfile, join
import time
import car_information_service
import json


def get_filenames_in_directory(directory):
    return [f.split(".")[0] for f in listdir(directory) if isfile(join(directory, f))]


def dump_json_to_file(directory, filepath, data):
    with open(join(directory, filepath + ".json"), "w") as outfile:
        outfile.write(json.dumps(data))


output_directory = "datasets/car_data"
img_directory = "datasets/car_images"
license_numbers = get_filenames_in_directory(img_directory)
for license_number in license_numbers:
    if not isfile(join(output_directory, license_number + ".json")):
        print(license_number)
        has_fetched = False
        try:
            car = car_information_service.get_car_information_from_api(
                license_number)
            has_fetched = True
        except:
            try:
                car = car_information_service.scrape_from_regnr(license_number)
                has_fetched = True
            except:
                print("Could not fetch information about :", license_number)
        finally:
            if has_fetched:
                dump_json_to_file(output_directory, license_number, car)
                print(json.dumps(car))
            time.sleep(1)
