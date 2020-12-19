FROM python:3.8-slim

WORKDIR /usr/src/app

# Python modules
COPY requirements.txt ./
RUN \
  pip3 install --upgrade setuptools && \
  pip3 install --no-cache-dir -r requirements.txt

# App
COPY app/ ./

CMD [ "python3", "main.py" ]
