import os
import shutil
from car_information_service import get_data_from_vegvesenet, \
    identify_license_plate
import sys


def safe_directory(directory):
    os.makedirs(directory, exist_ok=True)


def copy_image(image, input_directory, output_directory):
    safe_directory(output_directory)
    shutil.copy(input_directory + image, output_directory + image)


def delete_file(filepath):
    os.unlink(filepath)


def init_output_directory(directory):
    safe_directory(directory)
    safe_directory(directory + "/color")
    safe_directory(directory + "/brand")
    safe_directory(directory + "/model")
    safe_directory(directory + "/unlabelled")


def label_image(car, image, input_directory, output_directory):
    print("Label brand")
    label_brand(car, image, input_directory, output_directory)
    print("Label color")
    label_color(car, image, input_directory, output_directory)
    print("Label model")
    label_model(car, image, input_directory, output_directory)


def label_brand(car, image, input_directory, output_directory):
    assert car["merke"]
    destination_path = output_directory + "/brand/" + car["merke"] + "/"
    copy_image(image, input_directory, destination_path)


def label_color(car, image, input_directory, output_directory):
    assert car["farge"]
    destination_path = output_directory + "/color/" + car["farge"] + "/"
    copy_image(image, input_directory, destination_path)


def label_model(car, image, input_directory, output_directory):
    assert car["modell"]
    destination_path = output_directory + "/model/" + car["modell"] + "/"
    copy_image(image, input_directory, destination_path)


if __name__ == "__main__":
    input_directory = sys.argv[1]
    output_directory = sys.argv[2]

    images = os.listdir(input_directory)
    init_output_directory(output_directory)

    for image in images:
        print("Identifying license plate for image " + image)
        license_plate = identify_license_plate(input_directory, image)
        if license_plate:
            print("Identified license plate: " + license_plate)
            print("Fetching data for license plate " + license_plate)
            car = get_data_from_vegvesenet(license_plate)
            print(car)
            print("Labels image into data sets")
            label_image(car, image, input_directory, output_directory)
        else:
            print("Could not identify license plate of image " + image)
            destination = output_directory + "/unlabelled/"
            copy_image(image, input_directory, destination)
        # delete_file(input_directory + image)
