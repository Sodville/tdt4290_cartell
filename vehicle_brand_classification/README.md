# Vehicle Brand Recognition


<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->
<!-- code_chunk_output -->

- [Vehicle Brand Recognition](#vehicle-brand-recognition)
  - [Dependencies](#dependencies)
  - [Usage](#usage)
    - [Fine-tuning](#fine-tuning)
    - [Analysis](#analysis)
    - [Demo](#demo)

<!-- /code_chunk_output -->


This repository contains the source and functionality for predicting the brand of cars. The list of brands that are supported are found in `brands.txt` – this list is based on statistics about the most popular car brands in Norway.

## Dependencies

All relevant dependencies can be installed through

```sh
$ pip install -r requirements.txt
```

It is recommended to run this from a virtual environment of choice(such as Anaconda, pipenv, virtualenv or others). This is to avoid possible dependency errors.

## Usage

### Fine-tuning

*This section can be ignored if you're not interested in fine-tuning your own model. You can alternatively download our model weights from [here](https://drive.google.com/open?id=1CXWGf2hj_sJXIsSE4wfqUOqIv-EsYf7x) if you want to skip this section.*

To fine-tune the model you first need to download a dataset.

We use the [Stanford Cars Dataset](https://ai.stanford.edu/~jkrause/cars/car_dataset.html) as baseline. It contains 16,185 images of 196 classes of cars, the data is split into 8,144 training images and 8,041 testing images, where each class has been split roughly in a 50-50 split.

It can be downloaded by running

```bash
$ wget http://imagenet.stanford.edu/internal/car196/cars_train.tgz
$ wget http://imagenet.stanford.edu/internal/car196/cars_test.tgz
$ wget --no-check-certificate https://ai.stanford.edu/~jkrause/cars/car_devkit.tgz
```

Once downloaded, you can run

```sh
$ python3 pre-process.py
```
To pre-process and extract the images in the correct format.

If you furthermore want to use our custom-made dataset, you need to download it from [here](https://drive.google.com/open?id=1Nf3t7yCKDoikNC1mTFrDndULcvmFnn5N). It is highly recommended to thereafter combine it with the Stanford Cars Dataset for better model results.

Finally, you can fine-tune the model by following the listed steps

* Specify the correct training and validation directories in `train.py`, by editing the variables `train_dir` and `val_dir`
* If desired, change the parameters, such as batch size, number of epochs, and so on, for the training procedure in `train.py`
* `$ python3 train.py`

The training procedure will checkpoint the models with the highest top-1 validation accuracy.

If you want to visualize during training, run in your terminal:
```bash
$ tensorboard --logdir path_to_current_dir/logs
```
You should now be able to see the training accuracies and losses in `localhost:6006` in your web browser.

### Analysis
To calculate the accuracy on a given test set and compute the corresponding confusion matrix you can run the following script
```bash
$ python3 analyze.py [-h] [-t TEST_PATH] [-m MODEL_PATH]
```
For more help use the `-h` flag.

### Demo
To run a demo of the model, where prediction is performed on an input image and a heatmap is optionally output, you can run the following:

```bash
$ python3 demo.py [-h] -i IMAGE_PATH [-m MODEL_PATH] [-hm]
```
If `-hm` is passed as an argument, the heatmap for the prediction will be created and saved in `heatmap.jpg`. For more help use the `-h` flag.
