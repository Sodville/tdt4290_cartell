import requests
from bs4 import BeautifulSoup


REGNR_ENDPOINT = "https://regnr.info/husker-ikke-hele-regnr?"
VEGVESENET_API_ENDPOINT = "https://www.vegvesen.no/ws/no/vegvesen/kjoretoy/" \
    + "kjoretoyoppslag/v1/kjennemerkeoppslag/kjoretoy/"


def scrape_from_regnr(license_plate):
    url_params = "s1=" + license_plate[0] \
        + "&s2=" + license_plate[1] \
        + "&s3=" + license_plate[2] \
        + "&s4=" + license_plate[3] \
        + "&s5=" + license_plate[4] \
        + "&s6=" + license_plate[5] \
        + "&s7=" + license_plate[6] \

    response = requests.get(REGNR_ENDPOINT + url_params)

    soup = BeautifulSoup(response.text, "html.parser")

    car_information = soup.find(id="huskerikke_right")
    car_information = car_information.contents[3]
    car_information = car_information.contents[0]
    car_information = car_information.contents[2]

    return {
        "registreringsnummer": license_plate,
        # assume all brands are one-worded
        "merke": car_information.contents[1].string.split(" ", 1)[0],
        "modell": car_information.contents[1].string.split(" ", 1)[1],
        "farge": car_information.contents[3].string
    }


def get_from_api(license_plate):

    response = requests.get(VEGVESENET_API_ENDPOINT + license_plate).json()

    return {
        "registreringsnummer": response["kjennemerke"],
        "merke": response["tekniskKjoretoy"]["merke"],
        "modell": response["tekniskKjoretoy"]["handelsbetegnelse"],
        "farge": response["tekniskKjoretoy"]["karosseri"]["farge"]
    }
