from unittest.mock import Mock

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web
import discord
from discord.errors import NotFound, Forbidden

from ..views import routes


USERS = {1001: "user-1", 1002: "user-2", 1100: "forbidden user"}
USERS_FORBIDDEN = [1100]
CHANNELS = {2001: "channel-1", 2002: "channel-2", 2100: "forbidden channel"}
CHANNELS_FORBIDDEN = [2100]


class DiscordChannel:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    async def send(self, content, embed=None):
        if content:
            assert isinstance(content, str)
        if embed:
            assert isinstance(embed, discord.Embed)
        if self.id in CHANNELS_FORBIDDEN:
            raise Forbidden(response=Mock(), message="Test:Forbidden channel")


class DiscordUser:
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name

    async def create_dm(self):
        if self.id in USERS_FORBIDDEN:
            return DiscordChannel(2100, "dm-2")
        else:
            return DiscordChannel(2101, "dm-1")


class DiscordStub:
    async def fetch_channel(self, channel_id):
        if channel_id in CHANNELS:
            if channel_id in CHANNELS_FORBIDDEN:
                raise Forbidden(response=Mock(), message="Test:Forbidden channel")
            return DiscordChannel(id=channel_id, name=CHANNELS[channel_id])
        raise NotFound(response=Mock(), message="Test:Unknown channel")

    async def fetch_user(self, user_id):
        if user_id in USERS:
            return DiscordUser(id=user_id, name=USERS[user_id])
        raise NotFound(response=Mock(), message="Test:Unknown user")


class TestOtherViews(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        app.add_routes(routes)
        app["discord_client"] = DiscordStub()
        return app

    @unittest_run_loop
    async def test_should_return_index(self):
        # when
        resp = await self.client.request("GET", "/")
        # then
        self.assertEqual(resp.status, 200)
        text = await resp.text()
        self.assertIn("Discord Bridge", text)


class TestPostChannelMessageView(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        app.add_routes(routes)
        app["discord_client"] = DiscordStub()
        return app

    @unittest_run_loop
    async def test_should_return_204_when_ok_content_only(self):
        # when
        resp = await self.client.request(
            "POST",
            "/send_channel_message",
            json={"channel_id": 2001, "content": "test_content"},
        )
        # then
        self.assertEqual(resp.status, 204)

    @unittest_run_loop
    async def test_should_return_204_when_ok_embed_only(self):
        # when
        resp = await self.client.request(
            "POST",
            "/send_channel_message",
            json={"channel_id": 2001, "embed": {"description": "dummy"}},
        )
        # then
        self.assertEqual(resp.status, 204)

    @unittest_run_loop
    async def test_should_return_204_when_ok_content_and_embed(self):
        # when
        resp = await self.client.request(
            "POST",
            "/send_channel_message",
            json={
                "channel_id": 2001,
                "content": "test_content",
                "embed": {"description": "dummy"},
            },
        )
        # then
        self.assertEqual(resp.status, 204)

    @unittest_run_loop
    async def test_should_return_400_when_mandatory_param_is_missing(self):
        # when
        resp = await self.client.request(
            "POST", "/send_channel_message", json={"content": "test_content"}
        )
        # then
        self.assertEqual(resp.status, 400)

    @unittest_run_loop
    async def test_should_return_400_when_both_content_and_embed_are_missing(self):
        # when
        resp = await self.client.request(
            "POST", "/send_channel_message", json={"channel_id": 2001}
        )
        # then
        self.assertEqual(resp.status, 400)

    @unittest_run_loop
    async def test_should_return_404_when_channel_is_unknown(self):
        # when
        resp = await self.client.request(
            "POST",
            "/send_channel_message",
            json={"channel_id": 666, "content": "test_content"},
        )
        # then
        self.assertEqual(resp.status, 404)

    @unittest_run_loop
    async def test_should_return_403_when_access_denied(self):
        # when
        resp = await self.client.request(
            "POST",
            "/send_channel_message",
            json={"channel_id": 2100, "content": "test_content"},
        )
        # then
        self.assertEqual(resp.status, 403)


class TestPostDirectMessageView(AioHTTPTestCase):
    async def get_application(self):
        app = web.Application()
        app.add_routes(routes)
        app["discord_client"] = DiscordStub()
        return app

    @unittest_run_loop
    async def test_should_return_204_when_ok_content_only(self):
        # when
        resp = await self.client.request(
            "POST",
            "/send_direct_message",
            json={"user_id": 1001, "content": "test_content"},
        )
        # then
        self.assertEqual(resp.status, 204)

    @unittest_run_loop
    async def test_should_return_204_when_ok_embed_only(self):
        # when
        resp = await self.client.request(
            "POST",
            "/send_direct_message",
            json={"user_id": 1001, "embed": {"description": "dummy"}},
        )
        # then
        self.assertEqual(resp.status, 204)

    @unittest_run_loop
    async def test_should_return_204_when_ok_content_and_embed(self):
        # when
        resp = await self.client.request(
            "POST",
            "/send_direct_message",
            json={
                "user_id": 1001,
                "content": "test_content",
                "embed": {"description": "dummy"},
            },
        )
        # then
        self.assertEqual(resp.status, 204)

    @unittest_run_loop
    async def test_should_return_400_when_mandatory_param_is_missing(self):
        # when
        resp = await self.client.request(
            "POST",
            "/send_direct_message",
            json={"content": "bla bla"},
        )
        # then
        self.assertEqual(resp.status, 400)

    @unittest_run_loop
    async def test_should_return_400_when_both_content_and_embed_are_missing(self):
        # when
        resp = await self.client.request(
            "POST", "/send_direct_message", json={"user_id": 1001}
        )
        # then
        self.assertEqual(resp.status, 400)

    @unittest_run_loop
    async def test_should_return_404_when_user_is_unknown(self):
        # when
        resp = await self.client.request(
            "POST",
            "/send_direct_message",
            json={"user_id": 666, "content": "test_content"},
        )
        # then
        self.assertEqual(resp.status, 404)

    @unittest_run_loop
    async def test_should_return_403_when_user_access_not_allowed(self):
        # when
        resp = await self.client.request(
            "POST",
            "/send_direct_message",
            json={"user_id": 1100, "content": "test_content"},
        )
        # then
        self.assertEqual(resp.status, 403)
