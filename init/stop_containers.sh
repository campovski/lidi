#! /bin/bash

# This script get's executed by cron to stop all containers.
# Did not find a better way because echoing the following command
# directly to crontab resulted in executing the $().

docker stop $(docker ps -q --filter "name=lidi_container_");