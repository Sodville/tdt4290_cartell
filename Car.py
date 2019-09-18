import json


class Car:

    def __init__(self):
        self.registreringsnummer = None
        self.merke = None
        self.modell = None
        self.farge = None

    def __repr__(self):
        return f'Car({self.registreringsnummer!r}, {self.merke!r}, {self.modell!r}, {self.farge!r})'
