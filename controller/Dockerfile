# Python Base Image from https://hub.docker.com/r/arm32v7/python/
FROM arm32v7/python:3

COPY requirements.txt /
RUN pip install -r requirements.txt

# RUN apt-get update && apt-get upgrade
RUN apt-get install -y curl
RUN curl -sSL https://get.docker.com/ | sh
# Copy the Python Script to blink LED
COPY . /app
WORKDIR /app/manager
# CMD ["ls"]
# Trigger Python script
CMD ["python", "manager.py"]
