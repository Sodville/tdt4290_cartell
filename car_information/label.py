import os
import shutil
from car_information_service import get_data_from_vegvesenet, \
    identify_license_plate, ServiceUnavailableException, \
    LicensePlateNotFoundException, LicensePlateNotDetectedException, \
    IllegalLicensePlateException, CarInformationNotLoadedException
import sys

NO_INFORMATION = "no_information"
ILLEGAL_LICENSE_PLATE = "illegal_license_plate"
NO_LICENSE_PLATE = "no_license_plate"

BRAND = "brand"
COLOR = "color"
MODEL = "model"
UNLABELLED = "unlabelled"


def safe_directory(directory):
    os.makedirs(directory, exist_ok=True)


def copy_image(image, input_directory, output_directory):
    safe_directory(output_directory)
    if not file_exists(output_directory, image):
        shutil.copy(os.path.join(input_directory, image), os.path.join(output_directory, image))
    else:
        print("File already exist. Skips labelling")


def file_exists(directory, file):
    return os.path.exists(os.path.join(directory, file))


def delete_file(filepath):
    os.unlink(filepath)


def label_image(car, image, source_directory, destination_directory):
    print("Labels image to brand, color, model")
    label_brand(car, image, source_directory, destination_directory)
    label_color(car, image, source_directory, destination_directory)
    label_model(car, image, source_directory, destination_directory)


def label_brand(car, image, source_directory, destination_directory):
    assert car["merke"]
    destination_directory = os.path.join(destination_directory, BRAND, car["merke"])
    copy_image(image, source_directory, destination_directory)


def label_color(car, image, source_directory, destination_directory):
    assert car["farge"]
    destination_directory = os.path.join(destination_directory, COLOR, car["farge"])
    copy_image(image, source_directory, destination_directory)


def label_model(car, image, source_directory, destination_directory):
    assert car["modell"]
    destination_directory = os.path.join(destination_directory, MODEL, car["modell"])
    copy_image(image, source_directory, destination_directory)


def label_exception(label, image, source_directory, destination_directory):
    print("Label image to " + label)
    destination = os.path.join(destination_directory, label)
    copy_image(image, source_directory, destination)


if __name__ == "__main__":
    image_directory = sys.argv[1]
    dataset_directory = sys.argv[2]

    images = os.listdir(image_directory)

    for image in images:
        car = None
        print("Identifying license plate for image " + image)
        try:
            license_plate = identify_license_plate(image_directory, image)
            print("Identified license plate: " + license_plate)
            print("Fetching data for license plate " + license_plate)
            car = get_data_from_vegvesenet(license_plate)
            print(car)
            label_image(car, image, image_directory, dataset_directory)
        except ServiceUnavailableException as e:
            print(e)
            label_exception(UNLABELLED, image, image_directory, dataset_directory)
            print("Exits script")
            break
        except LicensePlateNotFoundException as e:
            print(e)
            label_exception(NO_LICENSE_PLATE, image, image_directory, dataset_directory)
        except LicensePlateNotDetectedException as e:
            print(e)
            label_exception(NO_LICENSE_PLATE, image, image_directory, dataset_directory)
        except IllegalLicensePlateException as e:
            print(e)
            label_exception(ILLEGAL_LICENSE_PLATE, image, image_directory, dataset_directory)
        except CarInformationNotLoadedException as e:
            print(e)
            label_exception(NO_INFORMATION, image, image_directory, dataset_directory)
        finally:
            delete_file(os.path.join(image_directory, image))

        print("")
