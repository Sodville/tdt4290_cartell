# -*- coding: utf-8 -*-

import argparse
import tarfile
import scipy.io
import numpy as np
import os
import cv2 as cv
import shutil
import random
from console_progressbar import ProgressBar

with open("brands.txt", "r") as f:
    brands = [line.strip().lower() for line in f.readlines()]

def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def is_data_present(dataset):
    if os.path.exists(f'data/{dataset}/train') and len(os.listdir(f'data/{dataset}/train')):
        return True
    if os.path.exists(f'data/{dataset}/valid') and len(os.listdir(f'data/{dataset}/valid')):
        return True
    if os.path.exists(f'data/{dataset}/test') and len(os.listdir(f'data/{dataset}/test')):
        return True
    return False

def get_brand_name(label):
    label = label[0][0].lower()
    for brand in brands:
        if brand in label:
            return brand
    return None

def save_train_data(fnames, labels, bboxes):
    src_folder = 'cars_train'
    num_samples = len(fnames)

    train_split = 0.8
    num_train = int(round(num_samples * train_split))
    train_indexes = random.sample(range(num_samples), num_train)

    pb = ProgressBar(total=100, prefix='Save train data', suffix='', decimals=3, length=50, fill='=')

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
        # print("{} -> {}".format(fname, label))
        pb.print_progress_bar((i + 1) * 100 / num_samples)

        if i in train_indexes:
            dst_folder = 'data/stanford/train'
        else:
            dst_folder = 'data/stanford/valid'

        dst_path = os.path.join(dst_folder, label)
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)
        dst_path = os.path.join(dst_path, fname)

        crop_image = src_image[y1:y2, x1:x2]
        dst_img = cv.resize(src=crop_image, dsize=(args.height, args.width))
        cv.imwrite(dst_path, dst_img)


def save_test_data(fnames, bboxes):
    src_folder = 'cars_test'
    dst_folder = 'data/stanford/test'
    num_samples = len(fnames)

    pb = ProgressBar(total=100, prefix='Save test data', suffix='', decimals=3, length=50, fill='=')

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
        # print(fname)
        pb.print_progress_bar((i + 1) * 100 / num_samples)

        dst_path = os.path.join(dst_folder, fname)
        crop_image = src_image[y1:y2, x1:x2]
        dst_img = cv.resize(src=crop_image, dsize=(args.height, args.width))
        cv.imwrite(dst_path, dst_img)


def process_train_data(class_names):
    print("Processing train data...")
    cars_annos = scipy.io.loadmat('devkit/cars_train_annos')
    annotations = cars_annos['annotations']
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
        brand = get_brand_name(class_name)
        if brand is None:
            continue
        labels.append(brand)
        fname = annotation[0][5][0]
        bboxes.append((bbox_x1, bbox_y1, bbox_x2, bbox_y2))
        fnames.append(fname)

    labels_count = np.unique(labels).shape[0]
    print(np.unique(labels))
    print('The number of different cars is %d' % labels_count)

    save_train_data(fnames, labels, bboxes)


def process_test_data(class_names):
    print("Processing test data...")
    cars_annos = scipy.io.loadmat('devkit/cars_test_annos')
    annotations = cars_annos['annotations']
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


def vmmr_save_data(src_folder, keep_models, class_cutoff, img_width, img_height, verbose):
    if not src_folder:
        print(f'No source directory for VMMR-dataset supplied, --vmmr_folder-argument required.')
        return
    
    labels = os.listdir(src_folder)
    num_train, num_valid, num_test, classes_skipped, classes_blacklisted = 0, 0, 0, 0, 0

    print(f'Splitting VMMR dataset into a test, validation and training set.')

    for label in labels:
        label_path = os.path.join(src_folder, label)
        filenames = os.listdir(label_path)
        n_images, n_test, n_valid = len(filenames), 0, 0


        # Check if class is whitelisted
        if label.split('_')[0] not in brands:
            if verbose:
                print(f'Skipping class {label} since brand is not whitelisted')
            classes_blacklisted += 1
            continue
        
        # Check if class has a premissible number of images
        if n_images < class_cutoff:
            if verbose:
                print(f'Skipping class {label} due to insufficient number of images ({n_images})')
            classes_skipped += 1
            continue

        if verbose:
            print(f'Preprocessing class {label}!')
        
        # Calculate number of test and validation images
        if n_images <= 10:
            n_test, n_valid = 1, 1
        else:
            n_test = round(n_images * 0.2)
            n_valid = round(n_images * 0.16)

        # Shuffle filenames to randomize images assigned to different sets
        random.shuffle(filenames)

        # Check whether to keep model and year information in the label
        if not keep_models:
            dst_label = label.split('_')[0]
        else:
            dst_label = label

        for fn in filenames:
            img = cv.imread(os.path.join(label_path, fn))
            if n_test > 0:
                dst_folder = 'data/vmmr/test'
                n_test -= 1
                num_test += 1
            elif n_valid > 0:
                dst_folder = 'data/vmmr/valid'
                n_valid -= 1
                num_valid += 1
            else:
                dst_folder = 'data/vmmr/train'
                num_train += 1
            
            dst_folder = os.path.join(dst_folder, dst_label)
            ensure_folder(dst_folder)
            dst_folder = os.path.join(dst_folder, fn)

            # Resize images
            img = cv.resize(src=img, dsize=(img_height, img_width))

            cv.imwrite(dst_folder, img)

    print((f'Dataset was split into a training set of {num_train} images, '
        f'a validation set of {num_valid} and a test set of {num_test}.'))
    print((f'{classes_blacklisted} classes were skipped due to brand not '
        f'being whitelisted and {classes_skipped} of classes with whitelisted '
        f'brand were skipped due to an image number less than cutoff {class_cutoff}.'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Preprocessing of image data.')
    parser.add_argument('--image_width', dest='width', type=int, default=224,
                        help='image width of resized images (default 224px)')
    parser.add_argument('--image_height', dest='height', type=int, default=224,
                        help='image height of resized images (default 224px)')
    parser.add_argument('dataset', choices=['stanford', 'vmmr'], 
                        help='which dataset to preprocess')
    parser.add_argument('--vmmr_folder', 
                        help='source folder containing the entire VMMRdb-dataset')
    parser.add_argument('--keep_models', action='store_true',
                        help='keep models in labels (e.g. volvo_v70, rather than just volvo)')
    parser.add_argument('--class_cutoff', type=int, default=5,
                        help='ignore classes that have less images than this (default 5)')
    parser.add_argument('-f', '--force', dest='force', action='store_true',
                        help='run preprocessing even if processed data is found, this might overwrite existing data')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='prints verbose output')

    args = parser.parse_args()
    dataset = args.dataset

    # Check whether processed data exists
    if not args.force and is_data_present(dataset):
        print(f'Found data in folder data/{dataset}. Aborting.')
        raise SystemExit()

    ensure_folder('data')
    ensure_folder(f'data/{dataset}')
    ensure_folder(f'data/{dataset}/train')
    ensure_folder(f'data/{dataset}/valid')
    ensure_folder(f'data/{dataset}/test')

    if dataset == 'stanford':
        print('Extracting cars_train.tgz...')
        if not os.path.exists('cars_train'):
            with tarfile.open('cars_train.tgz', "r:gz") as tar:
                tar.extractall()
        print('Extracting cars_test.tgz...')
        if not os.path.exists('cars_test'):
            with tarfile.open('cars_test.tgz', "r:gz") as tar:
                tar.extractall()
        print('Extracting car_devkit.tgz...')
        if not os.path.exists('devkit'):
            with tarfile.open('car_devkit.tgz', "r:gz") as tar:
                tar.extractall()

        cars_meta = scipy.io.loadmat('devkit/cars_meta')
        class_names = cars_meta['class_names']  # shape=(1, 196)
        class_names = np.transpose(class_names)
        print('class_names.shape: ' + str(class_names.shape))
        print('Sample class_name: [{}]'.format(class_names[8][0][0]))

        process_train_data(class_names)
        process_test_data(class_names)

        # clean up
        shutil.rmtree('cars_train')
        shutil.rmtree('cars_test')
        shutil.rmtree('devkit')

    elif dataset == 'vmmr':
        vmmr_save_data(args.vmmr_folder, args.keep_models, args.class_cutoff, args.width, args.height, args.verbose)

    else:
        print(f'Unexpected dataset-argument {dataset}!')
