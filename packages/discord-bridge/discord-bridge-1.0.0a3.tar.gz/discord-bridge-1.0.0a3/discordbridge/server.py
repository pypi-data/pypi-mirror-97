import argparse
import logging
import logging.config
import os
from pathlib import Path
import sys

from aiohttp import web
import discord

from . import __title__, __version__, constants
from .views import routes


logger = logging.getLogger(__name__)
_LOG_FILE_NAME = "discordbridgesrv.log"


def setup_server(args_list: list) -> tuple:
    """parses all command line arguments and configures logging"""
    my_args = _parse_args(args_list)
    token = (
        os.environ.get("DISCORD_BOT_TOKEN") if my_args.token is None else my_args.token
    )
    if not token:
        print("ERROR: No Discord bot token provided")
        exit(1)
    logging.config.dictConfig(_logging_config(my_args))
    return token, my_args


def _parse_args(args_list: list) -> argparse.ArgumentParser:
    """returns parsed command line arguments"""
    my_arg_parser = argparse.ArgumentParser(
        description="Server with HTTP API for sending messages to Discord",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    my_arg_parser.add_argument(
        "--token",
        help=(
            "Discord bot token. Can alternatively be specified as "
            "environment variable DISCORD_BOT_TOKEN."
        ),
    )
    my_arg_parser.add_argument(
        "--host", default=constants.DEFAULT_HOST, help="server host address"
    )
    my_arg_parser.add_argument(
        "--port", type=int, default=constants.DEFAULT_PORT, help="server port"
    )
    my_arg_parser.add_argument(
        "--log-level",
        default="INFO",
        help="Log level of log file",
        choices=["INFO", "WARN", "ERROR", "CRITICAL"],
    )
    my_arg_parser.add_argument(
        "--log-file-path",
        help=(
            "Path for storing the log file. If no path if provided, "
            "the log file will be stored in the current working folder"
        ),
    )
    my_arg_parser.add_argument(
        "--version",
        help="show the program version and exit",
        action="version",
        version=__version__,
    )
    return my_arg_parser.parse_args(args_list)


def _logging_config(my_args) -> dict:
    """returns dict to configure logging based on parsed args"""
    file_log_path_full = my_args.log_file_path
    filename = (
        Path(file_log_path_full) / _LOG_FILE_NAME
        if file_log_path_full
        else Path.cwd() / _LOG_FILE_NAME
    )
    print(f"Writing logfile to: {filename}")
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {"format": "[%(levelname)s] %(message)s"},
            "file": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        },
        "handlers": {
            "console": {
                "level": "CRITICAL",
                "formatter": "console",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",  # Default is stderr
            },
            "file": {
                "level": my_args.log_level,
                "formatter": "file",
                "class": "logging.FileHandler",
                "filename": str(filename),
                "mode": "a",
            },
        },
        "loggers": {
            "": {  # root logger
                "handlers": ["console", "file"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }


def run_server(token, my_args):
    """runs the server with given configuration until terminated"""
    discord.VoiceClient.warn_nacl = False
    client = discord.Client()
    try:
        client.loop.create_task(client.start(token))
        app = web.Application()
        app.add_routes(routes)
        app["discord_client"] = client
        logger.info("Starting server on http://%s:%s", my_args.host, my_args.port)
        web.run_app(app, host=my_args.host, port=my_args.port)
    except Exception:
        client.loop.run_until_complete(client.logout())
    finally:
        logger.info("Shutting down server")
        client.loop.close()


def main():
    """main function for starting the server"""
    print(f"{__title__} v{__version__}")
    print()
    run_server(*setup_server(sys.argv[1:]))


if __name__ == "__main__":
    main()
