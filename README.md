# How to run. 

First install `paho-mqtt` [documentation](https://pypi.org/project/paho-mqtt/) for python dependency. 

This is a publication and subscription approach. There are other approaches you can take. (Server/client, just polling, file way etc)

You need to install `mosquitto` first to be the broker. You can install it from here [link](https://www.mosquitto.org/download/)
In one terminal open the 
```
python script_handler.py
```

In another open
```
python video.py
```