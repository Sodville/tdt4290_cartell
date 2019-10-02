import cv2 as cv

from resnet_152 import resnet152_model

def load_model(weights_path, num_classes=32):
    img_width, img_height = 224, 224
    num_channels = 3
    model = resnet152_model(img_height, img_width, num_channels, num_classes)
    model.load_weights(weights_path, by_name=True)
    return model

def draw_str(dst, target, s):
    x, y = target
    cv.putText(dst, s, (x + 1, y + 1), cv.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=2, lineType=cv.LINE_AA)
    cv.putText(dst, s, (x, y), cv.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv.LINE_AA)

def plot_model(model):
    from keras.utils import plot_model
    plot_model(model, to_file='model.svg', show_layer_names=True, show_shapes=True)
