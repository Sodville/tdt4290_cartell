FROM tensorflow/tensorflow:1.12.0-py3

EXPOSE 5000

COPY efficientnetb0_512.hdf5 /app
COPY brands.txt /app

COPY ../requirements.txt /app
COPY ../api_setup.py /app
COPY ../api_upload.py /app
COPY ../model_utils.py /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "./api_upload.py,", "-w efficientnetb0_512.hdf5", "-b brand.txt"]
