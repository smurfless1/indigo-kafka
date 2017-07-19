#!/bin/bash

# explicitly use the system python - this only affects this script
PATH=/usr/bin:/bin:/usr/sbin:/sbin

# make sure pip is around
sudo easy_install pip

# same, but for kafka
sudo /usr/local/bin/pip install kafka-python
sudo /usr/local/bin/pip install kafka-python --upgrade


