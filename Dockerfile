# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:3

# Copy the Python Script to blink LED
COPY ./src ./
COPY ./logs ./
COPY ./cfg ./

# Intall the rpi.gpio python module
# RUN pip install --no-cache-dir rpi.gpio
COPY requirements.txt ./
# RUN apt-get install build-essential
RUN pip install -r requirements.txt

# Trigger Python script
CMD ["python", "./main.py"]