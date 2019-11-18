FROM tensorflow/tensorflow:1.12.0-py3

EXPOSE 5000

COPY . /app
# The weights are re-copied as to give an error if they are not present
COPY efficientnetb0_512.hdf5 /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "./api_upload.py"]
