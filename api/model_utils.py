import keras
import efficientnet.keras as efn
from PIL import Image
import io

def get_brands(brands_path):
    brands = None
    with open(brands_path, "r") as f:
        brands = [line.strip() for line in f.readlines()]
        brands = sorted(brands)
    return brands

def load_image(encoded_img, target_size=(512, 512)):
    img = Image.open(io.BytesIO(encoded_img))
    img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    img_array = keras.preprocessing.image.img_to_array(img)
    return img_array

def load_model(weights_path):
    model = keras.models.load_model(weights_path)
    model._make_predict_function() # to fix weird Keras error with Flask about missing Tensor
    return model

def decode_prediction(brands, pred):
    decoded_pred = dict()
    for i, prob in enumerate(pred):
        decoded_pred[brands[i]] = prob
    return decoded_pred

def predict(model, image, brands):
    image = image / 255.
    pred = model.predict(image[None, :, :, :])
    decoded_pred = decode_prediction(brands, pred[0])
    print(decoded_pred)
    return decoded_pred
