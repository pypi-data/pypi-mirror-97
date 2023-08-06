import json
import unittest
from urllib.parse import urljoin

import requests_mock
from requests.exceptions import ConnectionError, ConnectTimeout

from .. import __title__, constants
from ..client import WebClient


@requests_mock.Mocker()
class WebClientTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._base_url = f"http://{constants.DEFAULT_HOST}:{constants.DEFAULT_PORT}"

    def _build_url(self, route: str = "") -> str:
        return urljoin(self._base_url, route)

    def test_should_create_client_when_server_available(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "GET", self._build_url(), status_code=200, text=__title__
        )
        # when
        client = WebClient()
        # then
        self.assertIsInstance(client, WebClient)

    def test_should_raise_OSError_when_server_not_available(self, requests_mocker):
        # given
        requests_mocker.register_uri("GET", self._build_url(), status_code=500)
        # when/then
        with self.assertRaises(OSError):
            WebClient()

    def test_should_create_client_when_server_not_available_and_ping_disabled(
        self, requests_mocker
    ):
        # given
        requests_mocker.register_uri(
            "GET", self._build_url(), status_code=200, text=__title__
        )
        # when
        client = WebClient(disable_ping=True)
        # then
        self.assertIsInstance(client, WebClient)

    def test_should_return_true_if_server_is_up(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "GET", self._build_url(), status_code=200, text=__title__
        )
        client = WebClient(disable_ping=True)
        # when
        result = client.ping()
        # then
        self.assertTrue(result)

    def test_should_return_false_if_wrong_server(self, requests_mocker):
        requests_mocker.register_uri(
            "GET", self._build_url(), status_code=200, text="wrong server"
        )
        client = WebClient(disable_ping=True)
        # when
        result = client.ping()
        # then
        self.assertFalse(result)

    def test_should_return_false_if_server_is_down_1(self, requests_mocker):
        requests_mocker.register_uri("GET", self._build_url(), status_code=500)
        client = WebClient(disable_ping=True)
        # when
        result = client.ping()
        # then
        self.assertFalse(result)

    def test_should_return_false_if_server_is_down_2(self, requests_mocker):
        requests_mocker.register_uri("GET", self._build_url(), exc=ConnectTimeout)
        client = WebClient(disable_ping=True)
        # when
        result = client.ping()
        # then
        self.assertFalse(result)

    def test_should_return_false_if_server_is_down_3(self, requests_mocker):
        requests_mocker.register_uri("GET", self._build_url(), exc=ConnectionError)
        client = WebClient(disable_ping=True)
        # when
        result = client.ping()
        # then
        self.assertFalse(result)

    def test_should_send_channel_message_content_only(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "POST", self._build_url("send_channel_message"), status_code=201
        )
        client = WebClient(disable_ping=True)
        # when
        client.send_channel_message(channel_id=1234, content="my message text")
        # then
        data = json.loads(requests_mocker.last_request.text)
        self.assertDictEqual(data, {"channel_id": 1234, "content": "my message text"})

    def test_should_send_channel_message_embed_only(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "POST", self._build_url("send_channel_message"), status_code=201
        )
        client = WebClient(disable_ping=True)
        # when
        client.send_channel_message(channel_id=1234, embed={"description": "dummy"})
        # then
        data = json.loads(requests_mocker.last_request.text)
        self.assertDictEqual(
            data, {"channel_id": 1234, "embed": {"description": "dummy"}}
        )

    def test_should_send_channel_message_content_and_embed(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "POST", self._build_url("send_channel_message"), status_code=201
        )
        client = WebClient(disable_ping=True)
        # when
        client.send_channel_message(
            channel_id=1234,
            content="my message text",
            embed={"description": "dummy"},
        )
        # then
        data = json.loads(requests_mocker.last_request.text)
        self.assertDictEqual(
            data,
            {
                "channel_id": 1234,
                "content": "my message text",
                "embed": {"description": "dummy"},
            },
        )

    def test_should_send_direct_message_contents_only(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "POST", self._build_url("send_direct_message"), status_code=201
        )
        client = WebClient(disable_ping=True)
        # when
        client.send_direct_message(user_id=42, content="my important text")
        # then
        data = json.loads(requests_mocker.last_request.text)
        self.assertDictEqual(data, {"user_id": 42, "content": "my important text"})

    def test_should_send_direct_message_embed_only(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "POST", self._build_url("send_direct_message"), status_code=201
        )
        client = WebClient(disable_ping=True)
        # when
        client.send_direct_message(user_id=42, embed={"description": "dummy"})
        # then
        data = json.loads(requests_mocker.last_request.text)
        self.assertDictEqual(data, {"user_id": 42, "embed": {"description": "dummy"}})

    def test_should_send_direct_message_contents_and_embed(self, requests_mocker):
        # given
        requests_mocker.register_uri(
            "POST", self._build_url("send_direct_message"), status_code=201
        )
        client = WebClient(disable_ping=True)
        # when
        client.send_direct_message(
            user_id=42,
            content="my important text",
            embed={"description": "dummy"},
        )
        # then
        data = json.loads(requests_mocker.last_request.text)
        self.assertDictEqual(
            data,
            {
                "user_id": 42,
                "content": "my important text",
                "embed": {"description": "dummy"},
            },
        )
