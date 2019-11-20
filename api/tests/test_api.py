from io import BytesIO
from api_upload import api_setup
from model_utils import load_model, get_labels
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
    response = client.post('/api', buffered=True,
                               content_type='multipart/form-data',
                               data={'NOT_FILE': (BytesIO(b'FAKE IMAGE DATA'), 'doesnt_matter.jpg')})
    assert response.status_code == 400
    assert response.content_type == "application/json"
    assert response.json["message"] == "No file part in the request"


def test_fileupload_full_test_run_model_return_correct_brand():
    client = get_client()
    api_upload.model = load_model("./vehicle_brand_classification/efficientnetb0_512.hdf5")
    api_upload.target_shape = api_upload.model.layers[0].input_shape[1:-1]
    api_upload.labels = get_labels("./vehicle_brand_classification/brands.txt")
    image = open('./tests/test_img.jpg', 'rb')
    response = client.post('/api', buffered=True,
                               content_type='multipart/form-data',
                               data={'file': (image, "image.jpg")})
    image.close()
    print("Response from the model:", str(response.json))
    assert response.status_code == 200
    max_label = max(response.json, key=lambda k: response.json[k])
    print("Best fit:", max_label, "with a probability with", response.json[max_label])
    assert max_label == "toyota"  # Check that the image matches
