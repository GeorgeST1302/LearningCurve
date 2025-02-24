#!/bin/bash

docker run -d -v mongodb_data:/data/db -p 27017:27017 --name mongodb mongo:latest
