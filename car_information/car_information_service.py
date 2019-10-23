import requests
import base64
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
        results = result_json["results"]

        if len(results) == 0:
            raise LicensePlateNotDetectedException("Could not detect any license plates")
          
        # If several plates are in the picture, choose the on that takes the most space  
        license_plate = get_largest_plate(results)

        if not is_valid_license_plate(license_plate):
            raise IllegalLicensePlateException("The license plate does not follow Norwegian convention")

        return license_plate
    finally:
        pass


def get_largest_plate(result_json):
    largest_plate = [0, 0]  # [0] is the plate index, [1] is the square size of the given plate
    for i in range(len(result_json)):
        vehicle_region = result_json[i].get("vehicle_region")
        plate_height = vehicle_region.get("height")
        plate_width = vehicle_region.get("width")
        plate_size = plate_height*plate_width
        if plate_size > largest_plate[1]:
            largest_plate[0] = i
            largest_plate[1] = plate_size
    return result_json[largest_plate[0]].get("plate")

def is_valid_license_plate(license_plate):
    for i in range(len(license_plate)):
        if i < 2 and license_plate[i].isdigit():
            return False
        if i > 2 and license_plate[i].isalpha():
            return False
    return True

def get_data_from_vegvesenet(license_plate):

    response = requests.get(VEGVESENET_API_ENDPOINT + license_plate).json()
    status = response.get("status")
    if status == 500:
        raise ServiceUnavailableException("Vegvesenet's service is not available. Used up quota of calls.")
    if status == 404:
        raise LicensePlateNotFoundException("No car registered with license plate: " + license_plate)

    car = Car()
    car = car.load_data_from_vegvesenet(response)
    if car.has_loaded_data():
        return car.get_data()
    else:
        raise CarInformationNotLoadedException("Could not load car information on license plate " + license_plate)


class CarInformationNotLoadedException(Exception):
    pass


class ServiceUnavailableException(Exception):
    pass


class LicensePlateNotFoundException(Exception):
    pass


class LicensePlateNotDetectedException(Exception):
    pass

  
class IllegalLicensePlateException(Exception):
    pass
