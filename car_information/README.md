# Car Information

We use [https://www.vegvesen.no/ws/no/vegvesen/kjoretoy/kjoretoyoppslag/v1/kjennemerkeoppslag/kjoretoy/]
to collect data about cars. In order to collect the data we need the
license plates of the car. For license plate detection we use
OpenALPR Watchman.

## Car Information Service

`car_information_service` has a function `get_data_from_vegvesenet`
that calls Vegvesenet's API and return data about the car. The
return value of this function is an object of the form
    
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

    python3 car_information_download.py [image_directory] [output_directory]

This will output all data as json-files in a flat 
folder structure into the specified output directory.