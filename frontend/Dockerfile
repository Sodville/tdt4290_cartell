FROM tensorflow/tensorflow:1.12.0-py3

EXPOSE 5000

COPY . /app
COPY efficientnetb0_512.hdf5 /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "./api_upload.py"]
