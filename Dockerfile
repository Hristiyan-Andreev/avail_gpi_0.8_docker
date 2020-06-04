# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:3

# Copy the Python Script to blink LED
COPY src/ /src/
COPY logs/ /logs/

# Intall the rpi.gpio python module
# RUN pip install --no-cache-dir rpi.gpio
COPY requirements.txt ./
# RUN apt-get install build-essential
RUN pip install -r requirements.txt

COPY config.json /src/config.json
# Trigger Python script
CMD ["python", "./src/main.py"]