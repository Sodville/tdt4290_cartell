import json


class Car:
    def __init__(self):
        self.registreringsnummer = None
        self.merke = None
        self.modell = None
        self.farge = None

    def __repr__(self):
        return "Car(" \
                f"{self.registreringsnummer!r}," \
                f"{self.merke!r},"\
                f"{self.modell!r},"\
                f"{self.farge!r}"\
                ")"

    def load_data_from_json(self, data):
        car_data = json.loads(data)
        self.registreringsnummer = car_data["registreringsnummer"]
        self.merke = car_data["merke"]
        self.modell = car_data["modell"]
        self.farge = car_data["farge"]
        return self

    def load_data_from_vegvesenet(self, data):
        self.registreringsnummer = data["kjennemerke"]
        self.merke = data["tekniskKjoretoy"]["merke"]
        self.modell = data["tekniskKjoretoy"]["handelsbetegnelse"]
        self.farge = data["tekniskKjoretoy"]["karosseri"]["farge"]
        return self

    def get_data(self):
        return {
            "registreringsnummer": self.registreringsnummer,
            "merke": self.merke,
            "modell": self.modell,
            "farge": self.farge
        }