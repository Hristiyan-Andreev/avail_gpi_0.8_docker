# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:3

COPY requirements.txt /
RUN pip install -r requirements.txt

# Copy the Python Script to blink LED
COPY . /app
WORKDIR /app/src
# RUN pip install --no-cache-dir rpi.gpio
# RUN apt-get install build-essential
# ENTRYPOINT [ "python3" ]
# Trigger Python script
# CMD ["ls"]
CMD ["python", "main.py"]