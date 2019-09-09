import argparse
import numpy as np
from keras.models import load_model
from keras.preprocessing import image

def make_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image_path', help='Image path', dest='image_path', required=True)
    parser.add_argument('-m', '--model_path', help='Model path', default='color_model.h5', dest='model_path')
    return parser

def load_image(img_path, out_size=(227,227)):
    img = image.load_img(img_path, target_size=out_size)
    img = image.img_to_array(img)
    img = img.reshape((1,) + img.shape)
    img = img/255.
    return img

def get_class_string(one_hot_vector):
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
