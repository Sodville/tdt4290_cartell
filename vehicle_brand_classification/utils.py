import cv2
import numpy as np
import keras.backend as K

def load_model(weights_path):
    """
    Load a model with weights from a specified weight file
    Args:
        weights_path: The path to the weight file

    Returns: The model specified by the weights file with loaded parameters.
    """
    import keras.models
    model = keras.models.load_model(weights_path)
    return model

def get_brands():
    """
    Loads all brands that represents the predicted classes.
    Args:

    Returns: A sorted list of of the used brands.
    """
    with open("brands.txt", "r") as f:
        brands = [line.strip() for line in f.readlines()]
    brands = sorted(brands)
    return brands

def draw_str(dst, target, s):
    """
    Draw a string in-place on an image
    Args:
        dst: The image to draw the string on.
        target: The target position to draw the string on, specified as a tuple (x,y)
        s: The string to draw.

    Returns: 
    """
    x, y = target
    cv2.putText(dst, s, (x + 1, y + 1), cv2.FONT_HERSHEY_PLAIN, 1.0, (0, 0, 0), thickness=2, lineType=cv2.LINE_AA)
    cv2.putText(dst, s, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 255, 255), lineType=cv2.LINE_AA)

def plot_model(model):
    """
    Plots the structure of a model and save it as "model.svg"
    Args:
        model: The keras model to plot.

    Returns: 
    """
    from keras.utils import plot_model
    plot_model(model, to_file="model.svg", show_layer_names=True, show_shapes=True)

def load_image(img_path, target_size):
    """
    Load an image and resizes it to a desired target size
    Args:
        img_path: The directory jpath to the inpat image.
        target_size: A tuple (width, height) representing the target size

    Returns: The loaded image as a np.array
    """
    from keras.preprocessing import image
    img = image.load_img(img_path, target_size=target_size)
    return image.img_to_array(img)

def get_activation_map(model, img_path, img_size=(224,224)):
    """
    Computes the class activation map for a model and image as described by Zhou et al. (2016):
    Assumes that the model has a global pooling layer before the final softmax layer.
    Args:
        model: The directory jpath to the inpat image.
        img_path: The directory path to the input image.
        img_size: The image size the image should be resized to.

    Returns: 
    """
    img = load_image(img_path, img_size)

    softmax_layer, final_conv_layer = model.layers[-1], model.layers[-3]
    class_weights = softmax_layer.get_weights()[0]
    get_output = K.function([model.input], [final_conv_layer.output, softmax_layer.output])
    [conv_outputs, pred] = get_output([img[None, :, :, :] / 255.])
    pred, conv_outputs = pred[0, :], conv_outputs[0, :, :, :]
    predicted_class = np.argmax(pred)

    cam = np.dot(conv_outputs, class_weights[:, predicted_class])
    cam /= np.max(cam)
    cam = cv2.resize(cam, img_size)

    heatmap = cv2.applyColorMap(np.uint8(255*cam), cv2.COLORMAP_JET)
    heatmap[np.where(cam < 0.2)] = 0
    out = 0.5*heatmap + cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite("heatmap.jpg", out)

def get_gradient_activation_map(model, img_path, img_size=(224,224)):
    """
    Computes the *gradient-weighted* class activation map for a model and image as described by Selvaraju et al. (2016)
    Assumes that the model has a global pooling layer before the final softmax layer.
    May give another output than `get_activation_map` 
    Args:
        model: The directory jpath to the inpat image.
        img_path: The directory path to the input image.
        img_size: The image size the image should be resized to.

    Returns: 
    """
    img = load_image(img_path, img_size)
    pred_cls = np.argmax(model.predict(img[None, :, :, :] / 255.))

    loss = model.output[0, pred_cls]
    conv_output = model.layers[-3].output
    grads = K.gradients(loss, conv_output)[0]
    gradient_function = K.function([model.input], [conv_output, grads])

    output, grads_val = gradient_function([img[None, :, :, :] / 255.])
    output, grads_val = output[0, :], grads_val[0, :, :, :]

    weights = np.mean(grads_val, axis=(0, 1))
    cam = np.dot(output, weights)

    # Process CAM
    cam = cv2.resize(cam, img_size)
    cam /= np.max(cam)
    heatmap = cv2.applyColorMap(np.uint8(255*cam), cv2.COLORMAP_JET)
    heatmap[np.where(cam < 0.2)] = 0

    out = 0.5*heatmap + cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    cv2.imwrite("heatmap2.jpg", out)
