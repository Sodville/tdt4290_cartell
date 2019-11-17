import argparse
import efficientnet.keras as efn
from utils import load_model, get_brands, load_image

WIDTH, HEIGHT = 512, 512
brands = get_brands()

def make_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image_path', help='Image path', dest='image_path', required=True)
    parser.add_argument('-m', '--model_path', help='Model path', default='efficientnetb0_512.hdf5', dest='model_path')
    return parser

if __name__ == '__main__':
    args = make_arg_parser().parse_args()
    model = load_model(args.model_path)

    img = load_image(args.image_path, (WIDTH, HEIGHT)) / 255.

    preds = model.predict(img[None, :, :, :])
    print(args.image_path, "predicted as",  brands[preds.argmax()], "with probability", preds.max())
