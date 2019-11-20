import argparse
import numpy as np
from keras.models import load_model
from keras.preprocessing import image


def make_arg_parser():
    """
    Creates an argument parser for the prediction script
    Args:

    Returns: the argument parser for the script
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image_path', help='Image path', dest='image_path', required=True)
    parser.add_argument('-m', '--model_path', help='Model path', default='color_model.h5', dest='model_path')
    return parser

def load_image(img_path, out_size=(227,227)):
    """
    Load an image from a given image path, normalizes it, and resizes it to a given output size
    Args:
        img_path: image path to input image
        out_size: desired output resolution for image, defaults to 227x227
    Returns: A normalized np.array of the given image.
    """
    img = image.load_img(img_path, target_size=out_size)
    img = image.img_to_array(img)
    img = img.reshape((1,) + img.shape)
    img = img/255.
    return img

def get_class_string(one_hot_vector):
    """
    Decodes a one hot vector to the actual class string
    Args:
        one_hot_vector: the one hot vector to decode
    Returns: The class string for the input vector
    """
    labels = ['black', 'blue', 'cyan', 'gray', 'green', 'red', 'white', 'yellow']
    labels = sorted(labels)
    idx = np.argmax(one_hot_vector)
    return labels[idx]

if __name__ == "__main__":
    args = make_arg_parser().parse_args()

    model = load_model(args.model_path)
    img = load_image(args.image_path)
    pred = model.predict(img)

    print(pred[0])
    print("The color of the car is", get_class_string(pred))
