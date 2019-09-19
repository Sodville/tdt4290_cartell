from os import listdir
from os.path import isfile, join
from car_information_service import get_from_api, scrape_from_regnr
import time
import json


OUTPUT_DIRECTORY = "datasets/car_data"
IMAGE_DIRECTORY = "datasets/car_images"


def get_filenames_in_directory(directory):
    filenames = []
    for file in listdir(directory):
        if isfile(join(directory, file)):
            filenames.append(file.split(".")[0])
    return filenames


def dump_json_to_file(directory, filepath, data):
    with open(join(directory, filepath + ".json"), "w") as outfile:
        outfile.write(json.dumps(data))


def fetch_data(license_numbers):
    for license_number in license_numbers:
        filename = join(OUTPUT_DIRECTORY, license_number + ".json")
        if not isfile(filename):
            print("Fetching data of license number: " + license_number)
            has_fetched = False
            try:
                car = get_from_api(license_number)
                has_fetched = True
            except:
                try:
                    car = scrape_from_regnr(license_number)
                    has_fetched = True
                except:
                    pass
            finally:
                if has_fetched:
                    dump_json_to_file(OUTPUT_DIRECTORY, license_number, car)
                    print("Fetch ok")
                    print(json.dumps(car))
                else:
                    print("Could not fetch data of: " license_number)
                time.sleep(1)

license_numbers = get_filenames_in_directory(IMAGE_DIRECTORY)
fetch_data(license_numbers)
