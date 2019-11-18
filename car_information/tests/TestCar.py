from car_information.model.Car import Car
import os.path
import json
import unittest


class TestCar(unittest.TestCase):
    def test_load_car_data(self):
        a = Car()
        b = Car()
        data = self.get_mock_car_data()
        a.load_data_from_json(json.dumps(data))
        self.assertNotEqual(a, b)

    def test_load_from_json(self):
        path = "car_information/tests/car_data"
        # path = "car_data"
        data = None
        try:
            data = self.read_from_json(path, "XX12345")
        except FileNotFoundError:  # In case the test is ran from another directory
            print("Didn't find file, trying backup location")
            path = "car_data"
            data = self.read_from_json(path, "XX12345")
        a = Car()
        a.load_data_from_json(json.dumps(data))
        b = Car()
        self.assertNotEqual(a, b)

    def read_from_json(self, directory, filepath):
        print(os.path.join(directory, filepath + ".json"))
        with open(os.path.join(directory, filepath + ".json")) as json_file:
            data = json.load(json_file)
        return data

    def get_mock_car_data(self):
        return {
            "registreringsnummer": "XX12345",
            "merke": "Volkswagen",
            "modell": "Caddy",
            "farge": "Ukjent"
        }


if __name__ == '__main__':
    unittest.main()
