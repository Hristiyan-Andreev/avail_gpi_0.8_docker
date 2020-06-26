#!/bin/sh
docker container run --rm --privileged --name "avail_gpi" -v /Projects/avail_gpi_0.8_docker/avail_gpi:/app -v /var/log/:/app/logs avail_gpi_0.8:v1.1
