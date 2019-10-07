# Vehicle Color Classification

This module contains the model for predicting the color of a vehicle.

The model is based on the work of Rachmada et al., described [here](https://arxiv.org/pdf/1510.07391.pdf), and is displayed below.
![model](https://raw.githubusercontent.com/beerboaa/Color-Classification-CNN/master/architecture.jpg)

## Installation

Spin up a virtual environment(such as virtualenv, pipenv or conda) and run
```sh
pip install -r requirements.txt
```

## Training 

The training and validation must be saved in the paths `./data/train` and `./data/val`, relative to this README file. Furthermore,
the labels of the provided data are the folders, so that all training data of black cars will be saved in e.g. `./data/train/black`, etc.

Once the dependencies are installed, and the data is set up properly, you can start the training procedure

```sh
python3 train.py
```

Parameters, such as the number of epochs, input image dimensions, and batch size can be changed in `train.py`. 


## Demo

Once you have the model weights available you can run prediction on your test images, to observe how the model performs on the provided data.

The prediction script can be run as following

```sh
python3 predict.py -i [PATH_TO_INPUT_IMAGE] -m [PATH_TO_MODEL_WEIGHTS]
```

The `-m` parameter is optional as the script by default assumes that the model weight is stored in the same dictionary as `predict.py` and is named `color_model.h5`.
So, for example, if you had an image named `tesla.jpg`, that you would like to perform prediction on, and the image is stored in the same folder as `predict.py`.
You can simply run the following, if `color_model.h5` is also in the same dictionary as previously mentioned

```sh
python3 predict.py -i tesla.jpg
```
