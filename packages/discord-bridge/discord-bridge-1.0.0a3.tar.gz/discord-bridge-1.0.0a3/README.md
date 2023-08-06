# discord-bridge

> **THIS IS WORK-IN-PROGRESS** - Not released for production use yet

HTTP bridge for the Discord API

[![release](https://img.shields.io/pypi/v/discord-bridge?label=release)](https://pypi.org/project/discord-bridge/)
[![python](https://img.shields.io/pypi/pyversions/discord-bridge)](https://pypi.org/project/discord-bridge/)
[![pipeline](https://gitlab.com/ErikKalkoken/discord-bridge/badges/master/pipeline.svg)](https://gitlab.com/ErikKalkoken/discord-bridge/-/pipelines)
[![coverage report](https://gitlab.com/ErikKalkoken/discord-bridge/badges/master/coverage.svg)](https://gitlab.com/ErikKalkoken/discord-bridge/-/commits/master)
[![license](https://img.shields.io/badge/license-MIT-green)](https://gitlab.com/ErikKalkoken/discord-bridge/-/blob/master/LICENSE)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![chat](https://img.shields.io/discord/790364535294132234)](https://discord.gg/zmh52wnfvM)

## Contents

- [Overview](#overview)
- [Features](#key-features)
- [Examples](#examples)
- [Installation](#installation)
- [Updating](#updating)
- [Server configuration](#server-configuration)
- [Change Log](CHANGELOG.md)

## Overview

The current Discord API provides a way to send direct messages to users via Websockets.

However, some applications do not directly support Websockets, which makes it difficult to implement a feature for sending direct messages. For example many Django sites only directly support the HTTP protocol.

Django Bridge solves this problem by allowing applications to send direct messages to Discord users with an HTTP API. This is accomplished by providing two main components:

- server: A microservice that provides a HTTP API for sending direct messages and channel messages to Discord
- client: A Python library, which provides easy access to the microservice API through a wrapper class for Python apps (optional)

> **Note**<br>While Discord Bridge has been initially developed as helper for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth) / Django apps, it has no Django dependencies and will work with any app that can use the HTTP API.

## Features

- HTTP API for sending direct messages to users and guild channels
- Client library in Python for easy access to the HTTP API
- Microservice is fully configurable and has logging
- Solid test coverage

## Examples

Here is an example that shows how simple it is to send a direct message to a Discord user with the provided client library.

```python
from discordbridge.client import WebClient

client = WebClient()
client.send_direct_message(user_id=1234, content="Hello there!")
```

## Installation

install from PyPI:

```bash
pip install discord-bridge
```

Add server to supervisor.conf:

```ini
[program:discordbridge]
command=/home/allianceserver/venv/auth/bin/discordbridgesrv --token "TOKEN"
directory=/home/allianceserver/myauth/log
user=allianceserver
numprocs=1
autostart=true
autorestart=true
stopwaitsecs=120
stdout_logfile=/home/allianceserver/myauth/log/discordbridgesrv_out.log
stderr_logfile=/home/allianceserver/myauth/log/discordbridgesrv_err.log
```

## Updating

tbd

## Server configuration

The microservice is designed to run via [supervisor](https://pypi.org/project/supervisor/) and can be configured with the below arguments. It comes with sensible defaults and will in most cases only need the Discord bot token to operate. The bot token can be provided with argument or environment variable.

```text
usage: discordbridgesrv [-h] [--token TOKEN] [--host HOST] [--port PORT]
                        [--log-level {INFO,WARN,ERROR,CRITICAL}]
                        [--log-file-path LOG_FILE_PATH] [--version]

Server with HTTP API for sending messages to Discord

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN         Discord bot token. Can alternatively be specified as
                        environment variable DISCORD_BOT_TOKEN. (default:
                        None)
  --host HOST           server host address (default: 127.0.0.1)
  --port PORT           server port (default: 9876)
  --log-level {INFO,WARN,ERROR,CRITICAL}
                        Log level of log file (default: INFO)
  --log-file-path LOG_FILE_PATH
                        Path for storing the log file. If no path if provided,
                        the log file will be stored in the current working
                        folder (default: None)
  --version             show the program version and exit
```
