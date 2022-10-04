# -*- coding: utf-8 -*-

import tarfile
import scipy.io
import numpy as np
import os
import cv2 as cv
import shutil
import random
from console_progressbar import ProgressBar
from utils import get_brands

def ensure_folder(folder):
    """
    Create a folder if it does not exist.
    Args:
        folder: The folder to ensure exists.

    Returns:
    """
    if not os.path.exists(folder):
        os.makedirs(folder)

def get_make_name(label):
    """
    Get the car make from a Stanford Cars Label
    Args:
        folder: The label to retrieve the make from

    Returns: A string representing the car make
    """
    label = label[0][0].lower()
    for brand in brands:
        if brand in label:
            return brand
    return None

def save_train_data(fnames, labels, bboxes):
    """
    Saves training data in a folder structure where the folder names are the labels.
    Args:
        fnames: The filenames of the files to save in the label structure.
        labels: Labels for the dataset
        bboxes: Bounding boxes

    Returns: 
    """
    src_folder = "cars_train"
    num_samples = len(fnames)

    train_split = 0.8
    num_train = int(round(num_samples * train_split))
    train_indexes = random.sample(range(num_samples), num_train)

    pb = ProgressBar(total=100, prefix="Save train data", suffix="", decimals=3, length=50, fill="=")

    for i in range(num_samples):
        fname = fnames[i]
        label = labels[i]
        (x1, y1, x2, y2) = bboxes[i]

        src_path = os.path.join(src_folder, fname)
        src_image = cv.imread(src_path)
        height, width = src_image.shape[:2]
        # margins of 16 pixels
        margin = 16
        x1 = max(0, x1 - margin)
        y1 = max(0, y1 - margin)
        x2 = min(x2 + margin, width)
        y2 = min(y2 + margin, height)
        pb.print_progress_bar((i + 1) * 100 / num_samples)

        if i in train_indexes:
            dst_folder = "data/train"
        else:
            dst_folder = "data/valid"

        dst_path = os.path.join(dst_folder, label)
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        dst_path = os.path.join(dst_path, fname)

        cv.imwrite(dst_path, src_image)


def save_test_data(fnames, bboxes):
    """
    Saves test data in a separate folder
    Args:
        fnames: The filenames of the files to save in the seperate folder.
        bboxes: Bounding boxes

    Returns: 
    """
    src_folder = "cars_test"
    dst_folder = "data/test"
    num_samples = len(fnames)

    pb = ProgressBar(total=100, prefix="Save test data", suffix="", decimals=3, length=50, fill="=")

    for i in range(num_samples):
        fname = fnames[i]
        (x1, y1, x2, y2) = bboxes[i]
        src_path = os.path.join(src_folder, fname)
        src_image = cv.imread(src_path)
        height, width = src_image.shape[:2]
        # margins of 16 pixels
        margin = 16
        x1 = max(0, x1 - margin)
        y1 = max(0, y1 - margin)
        x2 = min(x2 + margin, width)
        y2 = min(y2 + margin, height)
        pb.print_progress_bar((i + 1) * 100 / num_samples)

        dst_path = os.path.join(dst_folder, fname)
        cv.imwrite(dst_path, src_image)

def process_train_data(class_names):
    """
    Process the training data and save them in a folder structure, with folders as labels.
    Args:
        class_names: The class names of the data.

    Returns: 
    """
    print("Processing train data...")
    cars_annos = scipy.io.loadmat("devkit/cars_train_annos")
    annotations = cars_annos["annotations"]
    annotations = np.transpose(annotations)

    fnames = []
    bboxes = []
    labels = []

    for annotation in annotations:
        bbox_x1 = annotation[0][0][0][0]
        bbox_y1 = annotation[0][1][0][0]
        bbox_x2 = annotation[0][2][0][0]
        bbox_y2 = annotation[0][3][0][0]
        class_name = class_names[annotation[0][4][0][0]-1]
        brand = get_make_name(class_name)
        if brand is None:
            continue
        labels.append(brand)
        fname = annotation[0][5][0]
        bboxes.append((bbox_x1, bbox_y1, bbox_x2, bbox_y2))
        fnames.append(fname)

    labels_count = np.unique(labels).shape[0]
    print(np.unique(labels))
    print("The number of different cars is %d" % labels_count)

    save_train_data(fnames, labels, bboxes)


def process_test_data():
    """
    Process the test data and save it in a folder structure, with folders as labels.
    Args:

    Returns: 
    """
    print("Processing test data...")
    cars_annos = scipy.io.loadmat("devkit/cars_test_annos")
    annotations = cars_annos["annotations"]
    annotations = np.transpose(annotations)

    fnames = []
    bboxes = []

    for annotation in annotations:
        bbox_x1 = annotation[0][0][0][0]
        bbox_y1 = annotation[0][1][0][0]
        bbox_x2 = annotation[0][2][0][0]
        bbox_y2 = annotation[0][3][0][0]
        fname = annotation[0][4][0]
        bboxes.append((bbox_x1, bbox_y1, bbox_x2, bbox_y2))
        fnames.append(fname)

    save_test_data(fnames, bboxes)

if __name__ == "__main__":
    # parameters
    img_width, img_height = 224, 224
    brands = get_brands()

    print("Extracting cars_train.tgz...")
    if not os.path.exists("cars_train"):
        with tarfile.open("cars_train.tgz", "r:gz") as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar)
    print("Extracting cars_test.tgz...")
    if not os.path.exists("cars_test"):
        with tarfile.open("cars_test.tgz", "r:gz") as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar)
    print("Extracting car_devkit.tgz...")
    if not os.path.exists("devkit"):
        with tarfile.open("car_devkit.tgz", "r:gz") as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar)

    cars_meta = scipy.io.loadmat("devkit/cars_meta")
    class_names = cars_meta["class_names"]  # shape=(1, 196)
    class_names = np.transpose(class_names)
    print("class_names.shape: " + str(class_names.shape))
    print("Sample class_name: [{}]".format(class_names[8][0][0]))

    ensure_folder("data/train")
    ensure_folder("data/valid")
    ensure_folder("data/test")

    process_train_data(class_names)
    process_test_data()

    # clean up
    shutil.rmtree("cars_train")
    shutil.rmtree("cars_test")
    shutil.rmtree("devkit")
