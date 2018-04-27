# BC2JsonPostPy

This script is mainly for simple project. Script reads data from [BigClown USB Dongle](https://www.bigclown.com/doc/interfaces/serial-port-json/). Data from USB Dongle are transformed to JSON object and send to URL using POST method. It is usable for differend integration platforms like [Microsoft Flow](https://flow.microsoft.com/).

## Configuration file

URL and MQTT parameters you can put to _config.ini_ file.

```
[DEFAULT]
URL = https://...
MQTT_SERVER = localhost
MQTT_PORT = 1883
```