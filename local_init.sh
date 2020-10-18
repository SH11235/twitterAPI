#!/bin/sh
if [ "$1" = "start" ]; then
	if [ "$2" = "no-cache" ]; then
		sudo docker build -t python_cgi -f docker/python_cgi/Dockerfile . --no-cache
	else
		sudo docker build -t python_cgi -f docker/python_cgi/Dockerfile .
	fi
	sudo docker run -d -p 8000:8000 python_cgi
elif [ "$1" = "stop" ]; then
	sudo docker kill $(sudo docker ps -q)
else
	echo "start: docker build && docker run, stop: docker kill"
fi
