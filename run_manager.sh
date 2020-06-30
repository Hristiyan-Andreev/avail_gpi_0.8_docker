#!/bin/sh
# Main directory without the last / - example /projects/avail_controller
AVAIL_WORKDIR="/Projects/avail_gpi_0.8_docker/avail_gpi"
# THe actual run command
docker container run --name "av_manager" -it --rm -e WORKDIR=$AVAIL_WORKDIR -v /var/run/docker.sock:/var/run/docker.sock -v /Projects/avail_gpi_0.8_docker/controller:/app -v /Projects/avail_gpi_0.8_docker/avail_gpi/cfg:/app/cfg -v /var/log:/app/logs av_controller:v1.1