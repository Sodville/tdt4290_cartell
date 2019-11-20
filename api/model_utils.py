import keras
import efficientnet.keras as efn
from PIL import Image
import io

def get_labels(labels_path):
    labels = None
    with open(labels_path, "r") as f:
        labels = [line.strip() for line in f.readlines()]
        labels = sorted(labels)
    return labels

def load_image(encoded_img, target_size=(512, 512)):
    img = Image.open(io.BytesIO(encoded_img))
    img = img.convert("RGB")
    img = img.resize(target_size, Image.NEAREST)
    img_array = keras.preprocessing.image.img_to_array(img)
    return img_array

def load_model(weights_path):
    model = keras.models.load_model(weights_path)
    model._make_predict_function() # to fix weird Keras error with Flask about missing Tensor
    return model

def decode_prediction(labels, pred):
    decoded_pred = dict()
    for i, prob in enumerate(pred):
        decoded_pred[labels[i]] = prob
    return decoded_pred

def predict(model, image, labels):
    image = image / 255.
    pred = model.predict(image[None, :, :, :])
    decoded_pred = decode_prediction(labels, pred[0])
    print(decoded_pred)
    return decoded_pred
