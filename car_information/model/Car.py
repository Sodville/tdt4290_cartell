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
        try:
            self.registreringsnummer = data["kjennemerke"]
            self.merke = data["tekniskKjoretoy"]["merke"]
            self.modell = data["tekniskKjoretoy"]["handelsbetegnelse"]
            self.farge = data["tekniskKjoretoy"]["karosseri"]["farge"]
        except KeyError:
            print("Could not load from vegvesenet")
            print(data)
        return self

    def has_loaded_data(self):
        return self.registreringsnummer and self.merke and self.modell and self.farge

    def get_data(self):
        return {
            "registreringsnummer": self.registreringsnummer,
            "merke": self.merke,
            "modell": self.modell,
            "farge": self.farge
        }