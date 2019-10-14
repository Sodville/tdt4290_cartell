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

We assume that every image in the image directory
has the license plate as the name, eg. `XX12345.json`.

We also assume that the output directory exists.

To locally download the data we run

    python3 download.py image_directory output_directory [output_directory_structure]

output_directory_structure can have four values:

* -C. This option will use the car colors as a label for 
the output directory.
* -B. This option will use the car brands as a label for
the output directory.
* -M. This option will use the car model as a label for
the output directory.
* Not defined. This option will not use any labels, thus
all data is in a flat folder structure.

## Unittests
How to run the unit tests

    python -m unittest

This will look for tests recursivly and then test them.
