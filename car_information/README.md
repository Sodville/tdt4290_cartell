# Car Information

We use Vegvesenet's API [https://www.vegvesen.no/ws/no/vegvesen/kjoretoy/kjoretoyoppslag/v1/kjennemerkeoppslag/kjoretoy/](https://www.vegvesen.no/ws/no/vegvesen/kjoretoy/kjoretoyoppslag/v1/kjennemerkeoppslag/kjoretoy/)
to collect data about cars. In order to collect data, we need the
license plates of the car. For license plate detection we use
OpenALPR Watchman.

## Car Information Service

`car_information_service` has a function `get_data_from_vegvesenet`
that calls Vegvesenet's API and returns data about the car. The
return value of this function is an object of the format
    
    {
        "registreringsnummer": "XX12345",
        "merke": "BRAND_NAME",
        "modell": "MODEL_NAME",
        "farge": "COLOR"
    }


## Generate data set from images

To locally label the data we run

    python3 label.py image_directory output_directory

The script will produce data sets with
three kinds of labels:
* Color
* Brand
* Model

Images where the license plates are not identified are
put into a directory with the name `unlabelled`.

## Unittests
How to run the unit tests

    python -m unittest

This will look for tests recursively and then test them.
