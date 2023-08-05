import json
import unittest

import requests_mock

from ..client import WebClient


@requests_mock.Mocker()
class WebClientTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.base_url = "http://127.0.0.1"
        self.port = 9100

    def test_should_create_client(self, requests_mocker):
        # when
        client = WebClient()
        # then
        self.assertIsInstance(client, WebClient)

    def test_should_return_true_if_server_is_up(self, requests_mocker):
        url = f"{self.base_url}:{self.port}/ping"
        requests_mocker.register_uri("GET", url, status_code=200)
        client = WebClient()
        # when
        result = client.ping()
        # then
        self.assertTrue(result)

    def test_should_return_false_if_server_is_down(self, requests_mocker):
        url = f"{self.base_url}:{self.port}/ping"
        requests_mocker.register_uri("GET", url, status_code=500)
        client = WebClient()
        # when
        result = client.ping()
        # then
        self.assertFalse(result)

    def test_should_send_channel_message_content_only(self, requests_mocker):
        # given
        url = f"{self.base_url}:{self.port}/post_channel_message"
        requests_mocker.register_uri("POST", url, status_code=201)
        client = WebClient()
        # when
        client.post_channel_message(channel_id=1234, content="my message text")
        # then
        data = json.loads(requests_mocker.last_request.text)
        self.assertDictEqual(data, {"channel_id": 1234, "content": "my message text"})

    def test_should_send_channel_message_embed_only(self, requests_mocker):
        # given
        url = f"{self.base_url}:{self.port}/post_channel_message"
        requests_mocker.register_uri("POST", url, status_code=201)
        client = WebClient()
        # when
        client.post_channel_message(channel_id=1234, embed={"description": "dummy"})
        # then
        data = json.loads(requests_mocker.last_request.text)
        self.assertDictEqual(
            data, {"channel_id": 1234, "embed": {"description": "dummy"}}
        )

    def test_should_send_channel_message_content_and_embed(self, requests_mocker):
        # given
        url = f"{self.base_url}:{self.port}/post_channel_message"
        requests_mocker.register_uri("POST", url, status_code=201)
        client = WebClient()
        # when
        client.post_channel_message(
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
        url = f"{self.base_url}:{self.port}/post_direct_message"
        requests_mocker.register_uri("POST", url, status_code=201)
        client = WebClient()
        # when
        client.post_direct_message(user_id=42, content="my important text")
        # then
        data = json.loads(requests_mocker.last_request.text)
        self.assertDictEqual(data, {"user_id": 42, "content": "my important text"})

    def test_should_send_direct_message_embed_only(self, requests_mocker):
        # given
        url = f"{self.base_url}:{self.port}/post_direct_message"
        requests_mocker.register_uri("POST", url, status_code=201)
        client = WebClient()
        # when
        client.post_direct_message(user_id=42, embed={"description": "dummy"})
        # then
        data = json.loads(requests_mocker.last_request.text)
        self.assertDictEqual(data, {"user_id": 42, "embed": {"description": "dummy"}})

    def test_should_send_direct_message_contents_and_embed(self, requests_mocker):
        # given
        url = f"{self.base_url}:{self.port}/post_direct_message"
        requests_mocker.register_uri("POST", url, status_code=201)
        client = WebClient()
        # when
        client.post_direct_message(
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
