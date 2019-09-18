import json


class Car:

    def __init__(self):
        self.registreringsnummer = None
        self.merke = None
        self.modell = None
        self.farge = None

    def __repr__(self):
        return f'Car({self.registreringsnummer!r}, {self.merke!r}, {self.modell!r}, {self.farge!r})'

    def load_data_from_json(self, data):
        car_data = json.loads(data)
        self.registreringsnummer = car_data["registreringsnummer"]
        self.merke = car_data["merke"]
        self.modell = car_data["modell"]
        self.farge = car_data["farge"]
