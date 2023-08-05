# discord-bridge

> **THIS IS WORK-IN-PROGRESS** Do not use in production

HTTP bridge for the Discord API

## Overview

The current Discord API provides a way to send direct messages to users via Websockets only.

However, some applications do not directly support Websockets, which makes it difficult to implement a feature for sending direct messages. For example many Django sites only support the HTTP protocol.

This micro server makes it easy to add this feature by providing direct message sending to Discord via a HTTP API.

## Features

- Can send direct messages to users and channels
- Client class that encapsulates all HTTP requests
- Easy to setup server, which is configurable and has logging
- Solid test coverage

## Examples

Here is an example that shows how simple it is to send a direct message to a Discord user with the provided client class.

```python
from discord_web_bridge.client import WebClient

client = WebClient()
client.send_direct_message(user_id=1234, content="Hello there!")
```

## Server configuration

The server is supposed to run via supervisor and can be configured with the below arguments. It comes with sensible defaults and will in most cases only need the Discord bot token to operate. The bot token can be provided with argument or environment variable.

```text
usage: server.py [-h] [--token TOKEN] [--host HOST] [--port PORT]
                 [--log-level {INFO,WARN,ERROR,CRITICAL}]
                 [--log-file-path LOG_FILE_PATH] [--version]

Server with HTTP API for sending messages to Discord

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN         Discord bot token. Can alternatively be specified as
                        environment variable DISCORD_BOT_TOKEN. (default:
                        None)
  --host HOST           server host address (default: 127.0.0.1)
  --port PORT           server port (default: 9100)
  --log-level {INFO,WARN,ERROR,CRITICAL}
                        Log level of log file (default: INFO)
  --log-file-path LOG_FILE_PATH
                        Path for storing the log file. If no path if provided,
                        the log file will be stored in the current working
                        folder (default: None)
  --version             show the program version and exit
```
