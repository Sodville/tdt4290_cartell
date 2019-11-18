# TDT4290-cartell

This repository contains all code for the TDT4290 project.


## Description

For more information on running the different codes, look at the README's inside the different folders.

| Module                       | Description                                                                                                  | Readme link |
|------------------------------|--------------------------------------------------------------------------------------------------------------|-------------|
| Vehicle brand classification | Code to train and predict vehicle brands from images.                                                        | [README.md](vehicle_brand_classification/README.md)  |
| Vehicle color classification | Code to train and predict vehicle colors from images.                                                        | [README.md](vehicle_color_classification/README.md)  |
| API                          | The API for receiving images and classifying them. Also contains the Dockerfile used when deploying the API. | [README.md](api/README.md)  |
| Labeling script              | The program to label images with the corresponding brand and color from license plates in images.            | [README.md](car_information/README.md)  |
| Azure custom vision          | The program used to upload a dataset to the Microsoft  Azure Custom Vision platform.                         | [README.md](azure_custom_vision/README.md)  |

## Setting up a virtual environment

To be able to run the project you need python 3.6 or higher.
When running the python code, it's recommend to use a virtual environment, but it is not required.
To setup a virtual environment, make sure that you have `python3-venv` installed.

The virtual environment can be initalized by running the commands:

```
python -m venv env
source env/bin/activate
```

To install the required modules, run the command:
```
pip install -r requirements.txt
```
