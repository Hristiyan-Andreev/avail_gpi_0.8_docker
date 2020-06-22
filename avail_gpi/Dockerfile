# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:3

COPY requirements.txt /
RUN pip install -r requirements.txt
ENV TZ="Europe/Sofia"

# Copy the Python Script to blink LED
COPY . /app
WORKDIR /app/src
# CMD ["ls"]
# Trigger Python script
CMD ["python", "main.py"]
