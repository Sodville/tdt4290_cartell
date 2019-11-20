FROM tensorflow/tensorflow:1.14.0-py3

EXPOSE 5000

ARG weights=./vehicle_brand_classification/efficientnetb0_512.hdf5
ARG labels=./vehicle_brand_classification/brands.txt

COPY ${weights} /app/weights.hdf5
COPY ${labels} /app/labels.txt

COPY ./requirements.txt /app
COPY ./api_setup.py /app
COPY ./api_upload.py /app
COPY ./model_utils.py /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "./api_upload.py", "-w", "weights.hdf5", "-l", "labels.txt"]
