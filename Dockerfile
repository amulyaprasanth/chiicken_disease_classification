FROM python:3.10-slim-buster

RUN apt update -y && apt install awscli -y

COPY . ./app
RUN pip install -r requirements.txt
RUN pip install conda
RUN conda install -c conda-forge cudatoolkit=11.2 cudnn=8.1.0

CMD [ "python3", "app.py" ]