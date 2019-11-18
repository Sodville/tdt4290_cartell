import os
import argparse

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix

import efficientnet.keras as efn
from utils import load_model, get_brands, get_activation_map, load_image

WIDTH, HEIGHT = 512, 512

def predict(img_dir, model, target_size=(224,224)):
    img_files = []
    for root, dirs, files in os.walk(img_dir, topdown=False):
        for name in files:
            img_files.append(os.path.join(root, name))
    img_files = sorted(img_files)

    y_pred, y_true = [], []
    for img_path in img_files:
        x = load_image(img_path, target_size) / 255.

        preds = model.predict(x[None, :, :, :])
        print(img_path, brands[preds.argmax()], preds.max())
        pred_label = brands[preds.argmax()]
        y_pred.append(pred_label)
        tokens = img_path.split(os.path.sep)
        class_id = tokens[-2]
        y_true.append(class_id)
    return y_pred, y_true

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    fig, ax = plt.subplots()

    img = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(img, ax=ax)
    # show all ticks
    ax.set(xticks=np.arange(cm.shape[1]),
       yticks=np.arange(cm.shape[0]),
       # ... and label them with the respective list entries
       xticklabels=classes, yticklabels=classes,
       title=title,
       ylabel='True label',
       xlabel='Predicted label'
    )
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")
    fig.tight_layout()

def calc_acc(y_pred, y_true):
    num_corrects = 0
    for i in range(num_samples):
        pred = y_pred[i]
        test = y_true[i]
        if pred == test:
            num_corrects += 1
    return num_corrects / num_samples

def make_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test_path', help='Test dir path', default="data/test", dest='test_path')
    parser.add_argument('-m', '--model_path', help='Model path', default='ef/efficientnetb0_512.hdf5', dest='model_path')
    return parser

if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    brands = get_brands()

    num_samples = sum([len(files) for _, _, files in os.walk(args.test_path)])
    print("\nLoading the fine-tuned model....")
    model = load_model(args.model_path)

    y_pred, y_true = predict(args.test_path, model, (WIDTH, HEIGHT))

    acc = calc_acc(y_pred, y_true)
    print("%s: %.2f%%" % ('acc', acc * 100))

    # Compute confusion matrix
    cnf_matrix = confusion_matrix(y_true, y_pred, labels=brands)
    np.set_printoptions(precision=2)

    # Plot non-normalized confusion matrix
    plot_confusion_matrix(cnf_matrix, classes=brands,
                          title='Confusion matrix, without normalization')

    # Plot normalized confusion matrix
    plot_confusion_matrix(cnf_matrix, classes=brands, normalize=True,
                          title='Normalized confusion matrix')

    plt.show()
