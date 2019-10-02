import os
import cv2
import keras.backend as K
import numpy as np

from utils import load_model

if __name__ == '__main__':
    img_width, img_height = 224, 224
    weights_path='models/model.26-0.95.hdf5'
    model = load_model(weights_path)

    with open("brands.txt", "r") as f:
        brands = [line.strip().lower() for line in f.readlines()]
    brands = sorted(brands)

    test_path = 'test/'
    test_images = [f for f in os.listdir(test_path)]
                   
    print(test_images)

    for i, image_name in enumerate(test_images):
        filename = os.path.join(test_path, image_name)
        print('Start processing image: {}'.format(filename))
        bgr_img = cv2.imread(filename)
        bgr_img = cv2.resize(bgr_img, (img_width, img_height), cv2.INTER_CUBIC)

        rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        rgb_img = np.expand_dims(rgb_img, 0)

        preds = model.predict(rgb_img)
        prob = np.max(preds)
        class_id = np.argmax(preds)

        print('Predict: {}, prob: {}'.format(brands[class_id], prob))

    K.clear_session()
