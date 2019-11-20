# API

The API is based on Flask, and can be used both locally and in a Docker-environment.

The Dockerfile creates a Docker image which contains an API and the model for use in prediction.
 

## Running locally

* Install dependencies
   ```py
   pip install -r requirements.txt
   ```

* Download weights for the model you want to use.
  * [Brand model weights](https://drive.google.com/file/d/1CXWGf2hj_sJXIsSE4wfqUOqIv-EsYf7x/view?usp=sharing)
  * [Color model weights](https://drive.google.com/file/d/1lRUEykbsTh3VXAQqPaILYLzWt2cDDsBP/view?usp=sharing)

* You should now be able to spin up the API:

  ```py
  python3 api_upload.py -w PATH_TO_WEIGHTS -l PATH_TO_LABELS
  ```

   `-w` is optional, and will by default refer respectively to weights to the model you want to load, so saving the weights in the same folder as `api_upload.py` without renaming the file will save you from specifying the path.
   `-l` is the path to the labels and can be `brands.txt` or `colors.txt` depending on if you downloaded the color or brand model weights.
   
 You should now be able to send POST requests of your images as jpg or png file formats. The request must be sent to port 5000.

 A succesful response with code 200 could look like the following for brand prediction
 ```
 {'audi': 1.5660635e-10, 'bmw': 5.7521644e-12, 'ford': 7.1362174e-12, 'jaguar': 7.3524025e-12, 'mercedes': 4.0594708e-11, 'mitsubishi': 3.221091e-14, 'nissan': 1.0, 'peugeot': 1.3644183e-11, 'porsche': 3.095818e-12, 'skoda': 1.0349395e-09, 'tesla': 2.1225747e-12, 'toyota': 1.0142925e-10, 'volkswagen': 4.066172e-12, 'volvo': 7.5269685e-10}
 ```

and for color prediction:
 ```
{ “black”: 5.854989102851937e-18, “blue”: 1.0627216710530196e-14, “cyan”: 8.173336139838394e-12, “gray”: 2.8952212263906596e-13, “green”: 2.851018052751897e-07, “red”: 4.1193661844260085e-14, “white”: 1.254491264388285e-15, “yellow”: 0.9999997615814209 }
 ```

## Running on Docker

The program Docker is needed for building and running the docker image.
Docker can be installed via the guide on [https://docs.docker.com/install](https://docs.docker.com/install/). 

To build the image, the only thing required will be the weights, which can either be downloaded from [here](https://drive.google.com/file/d/1CXWGf2hj_sJXIsSE4wfqUOqIv-EsYf7x/view?usp=sharing) for brand prediction, or [here](https://drive.google.com/file/d/1lRUEykbsTh3VXAQqPaILYLzWt2cDDsBP/view?usp=sharing) for color prediction, or created as described in the corresponding vehicle classification [README.md](../README.md).


### Build image

The image can be build with either the brand classification weights, or the color classification weights.

To build the brand classification image run:
```
docker build -t api_brand --build-arg weights=./vehicle_brand_classification/efficientnetb0_512.hdf5 --build-arg labels=./vehicle_brand_classification/brands.txt .
```

The color classification image can be made with:
```
 docker build -t api_color --build-arg weights=./vehicle_color_classification/color_weights.hdf5 --build-arg labels=./vehicle_color_classification/colors.txt .
```

### Run image
After the image is created, it can be used by running command:
```
docker run -p 5000:5000 api_brand:latest
```
or for color prediction:
```
docker run -p 5000:5000 api_color:latest
```

Add `-d` to detach it from the terminal and make in run in the background.


### Run tests
To run the tests, the requirements are located in tests/requirements.txt. 
The tests also require the weights and labels for the models.
```
pip3 install -r tests/requirements.txt
```
To run the tests for the API, run this command inside the api folder:
```
python3 -m pytest tests
```

## API documentation

**URL-Endpoint: `GET /liveness`**

This endpoint checks if the system is responsive and is up and running.


**Success response:**
```
Code: 200
Content: OK
```


**URL-Endpoint: `POST /api`**

This endpoint is used for car classification. Both the 
car color and car make classification uses the same api endpoint.
The responses will be similar, only the labels will be different.


Request-body:
```
POST /api HTTP/1.1
Accepts: application/json
Content-Type: multipart/form-data

Content-Disposition: form-data; name="file"; filename=<IMAGE_PATH>
```

Curl example:
```
curl -X POST \
  http://0.0.0.0:5000/api \
  -H 'content-type: multipart/form-data' \
  -F file=@test_img.jpg
```

**Sucess response (car make classfication):**
```
Code: 200
Content-Type: application/json
Content: {
  "audi": 1.8454512362708897e-9,
  "bmw": 1.8632862008871598e-7,
  "ford": 4.905129080690074e-10,
  "jaguar": 4.323361224578548e-8,
  "mercedes": 1.5409258591336794e-10,
  "mitsubishi": 3.721137981083089e-12,
  "nissan": 6.927771689646534e-10,
  "peugeot": 1.4581404139679677e-10,
  "porsche": 5.530252904922817e-12,
  "skoda": 0.00008143833838403225,
  "tesla": 1.6919127774142617e-12,
  "toyota": 0.9997408986091614,
  "volkswagen": 0.0001774589909473434,
  "volvo": 5.509662170943841e-11
}
```

**Success response (car color classification):**
```
Code: 200
Content-Type: application/json
Content: {
{
    “black”: 5.854989102851937e-18,
    “blue”: 1.0627216710530196e-14,
    “cyan”: 8.173336139838394e-12,
    “gray”: 2.8952212263906596e-13,
    “green”: 2.851018052751897e-07,
    “red”: 4.1193661844260085e-14,
    “white”: 1.254491264388285e-15,
    “yellow”: 0.9999997615814209
}
```

Error responses:
```
Code: 400
Content-Type: application/json
Content: "Bad request"
```