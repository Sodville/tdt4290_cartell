from io import BytesIO
from api_upload import api_setup
from model_utils import load_model, get_brands
import api_upload
import pytest


def get_client():
    client = api_setup.test_client()
    client.testing = True
    return client


def test_liveness_return_ok():
    client = get_client()
    response = client.get("/liveness")
    assert response.status_code == 200
    assert response.data.decode("utf-8") == "OK"


def test_fileupload_wrong_post_argument_return_error():
    client = get_client()
    response = client.post('/file-upload', buffered=True,
                               content_type='multipart/form-data',
                               data={'NOT_FILE': (BytesIO(b'FAKE IMAGE DATA'), 'bad_img.jpg')})
    assert response.status_code == 400
    assert response.content_type == "application/json"
    assert response.json["message"] == "No file part in the request"


def test_fileupload_full_test_run_model_return_correct_brand():
    client = get_client()
    api_upload.model = load_model("./efficientnetb0_512.hdf5")
    api_upload.brands = get_brands("./brands.txt")
    image = open('./tests/test_img.jpg', 'rb')
    response = client.post('/file-upload', buffered=True,
                               content_type='multipart/form-data',
                               data={'file': (image, "image.jpg")})
    image.close()
    print("Response from the model:", str(response.json))
    assert response.status_code == 201
    max_brand = max(response.json, key=lambda k: response.json[k])
    print("Best fit:", max_brand, "with a probability with", response.json[max_brand])
    assert max_brand == "toyota"  # Check that the image matches
