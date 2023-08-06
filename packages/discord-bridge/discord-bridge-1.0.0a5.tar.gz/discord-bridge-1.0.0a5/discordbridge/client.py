import logging
from urllib.parse import urljoin

import requests
from requests.exceptions import RequestException
from . import __title__, constants

logger = logging.getLogger(__name__)


class WebClient:
    """Client for using the Web API of the Discord Bridge server"""

    def __init__(
        self,
        host: str = constants.DEFAULT_HOST,
        port: int = constants.DEFAULT_PORT,
        timeout=constants.DEFAULT_CLIENT_TIMEOUT,
        disable_ping=False,
    ) -> None:
        """Connects to the server

        Args:
            host: host address the bridge server is running on
            port: port the bridge server is running on
            timeout: connection timeout in seconds
            disable_ping: set True to disable initial server ping

        Exceptions:
            OSError: in case the server is not up
        """
        self._base_url = f"http://{str(host)}:{int(port)}"
        self._timeout = timeout
        if not disable_ping and not self.ping():
            raise OSError(f"Server not reachable at {self._base_url}")

    def _build_url(self, route: str = "") -> str:
        return urljoin(self._base_url, str(route))

    def ping(self) -> bool:
        """Checks if the server is up

        Returns:
            True if the server is up, else False
        """
        try:
            r = requests.get(self._build_url(), timeout=self._timeout)
        except RequestException:
            return False
        return True if r.ok and __title__ in r.text else False

    def send_channel_message(
        self, channel_id: int, content: str = None, embed: dict = None
    ) -> None:
        """posts a message in the given channel

        Args:
            channel_id: Discord ID of the channel
            content: message text
            embed: embed to add to the message (see Discord API documentation for correct format)

        Exceptions:
            requests.exceptions.HTTPError: 404: Channel not found

        """
        params = {
            "channel_id": int(channel_id),
        }
        if content:
            params["content"] = str(content)
        if embed:
            params["embed"] = embed
        r = requests.post(
            self._build_url("send_channel_message"),
            json=params,
            timeout=self._timeout,
        )
        r.raise_for_status()

    def send_direct_message(
        self, user_id: int, content: str = None, embed: dict = None
    ):
        """posts a direct message to a user

        Args:
            user_id: Discord ID of the user
            content: message text
            embed: embed to add to the message (see Discord API documentation for correct format)

        Exceptions:
            requests.exceptions.HTTPError: 404: User not found

        """
        params = {
            "user_id": int(user_id),
        }
        if content:
            params["content"] = str(content)
        if embed:
            params["embed"] = embed
        r = requests.post(
            self._build_url("send_direct_message"),
            json=params,
            timeout=self._timeout,
        )
        r.raise_for_status()
