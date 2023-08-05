import logging
from urllib.parse import urljoin

import requests
from . import constants

logger = logging.getLogger(__name__)


class WebClient:
    """Client for using the Web API of the Discord Bridge server"""

    TIMEOUT_DEFAULT = 1

    def __init__(
        self, host: str = constants.DEFAULT_HOST, port: int = constants.DEFAULT_PORT
    ) -> None:
        """Create a new instance

        Args:
            host: host address the bridge server is running on
            port: port the bridge server is running on
        """
        self._base_url = f"http://{str(host)}:{int(port)}"

    def _build_url(self, route: str) -> str:
        return urljoin(self._base_url, str(route))

    def ping(self) -> bool:
        r = requests.get(self._build_url("ping"), timeout=self.TIMEOUT_DEFAULT)
        return True if r.ok else False

    def post_channel_message(
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
            self._build_url("post_channel_message"),
            json=params,
            timeout=self.TIMEOUT_DEFAULT,
        )
        r.raise_for_status()

    def post_direct_message(
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
            self._build_url("post_direct_message"),
            json=params,
            timeout=self.TIMEOUT_DEFAULT,
        )
        r.raise_for_status()
