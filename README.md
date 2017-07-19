Indigo Plug-In for Kafka
---

Indigo Plug-In for writing JSON to Apache Kafka topics. 

Before starting
---

* Install/license Indigo 7

Configure Indigo
---

* Open and read the install_python_modules.sh script. This will be modifying the system python, unless someone has a cooler way of doing this later.
* Run the script install_python_modules.sh and restart the Indigo server process.  THIS REALLY HAS TO BE DONE BEFORE INSTALLING THE PLUGINS.  Stop and restart the indigo server from the UI so it can learn about the new modules.  I hate this step, but there you go. 
* Install the plugin by double-clicking. 
* Configure the hostname/user/pass/ports etc. For me the defaults for the local system are already set.
* Go get a drink, turning switches on and off along the way, setting off motion sensors, opening doors, and generally being disruptive. 


But I don't have Kafka
---

If you don't have a kafka instance, you CAN install it on your mac, use docker, use real hardware, etc. Let's walk through installing a homebrew kafka.

* Install homebrew : https://brew.sh/
* Install homebrew services:

```
brew update
# use https://github.com/Homebrew/homebrew-services
brew tap homebrew/services
brew install kafka
```

* Configuring kafka is a big topic - be very happy that it mostly will just work straight from homebrew.

```
brew services start kafka
```

Kafka is a big topic all its own. Use the readme from Apache to continue if you don't know your way around. We're publishing one record per message, just json.

