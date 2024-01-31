#!/bin/bash

source /home/pi/Firmware/gRPC/bin/activate

python -m pip install grpcio --no-cache-dir

python3 /home/pi/Firmware/gRPC/app/client.py