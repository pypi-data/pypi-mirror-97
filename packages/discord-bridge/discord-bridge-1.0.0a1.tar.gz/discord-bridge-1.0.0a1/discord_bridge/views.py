import logging

from aiohttp import web
import discord
from discord.errors import NotFound

from . import __title__, __version__

logger = logging.getLogger(__name__)
routes = web.RouteTableDef()


@routes.get("/")
async def index(request):
    return web.Response(text=f"{__title__} v{__version__}")


@routes.get("/ping")
async def ping(request):
    """Simple view to check if the server is up

    Format:
        HTTP GET

    Returns:
        HTTP 204 on success, else raises HTTP exception
    """
    return web.Response(status=204)


@routes.post("/post_channel_message")
async def post_channel_message(request):
    """Posts a message in any guild channel.

    Format:
        HTTP POST with JSON body

    Args:
        channel_id: Discord ID of the channel
        content: message text (Optional)
        embed: embed to add to the message (Optional) (see Discord API documentation for correct format)

    Returns:
        HTTP 204 on success, else raises HTTP exception
    """
    data = await request.json()
    content = data.get("content")
    embed_dict = data.get("embed")
    if "channel_id" not in data or (not content and not embed_dict):
        raise web.HTTPBadRequest()
    discord_client = request.app["discord_client"]
    try:
        channel = await discord_client.fetch_channel(channel_id=data["channel_id"])
    except NotFound as ex:
        raise web.HTTPNotFound() from ex
    embed = discord.Embed.from_dict(embed_dict) if embed_dict else None
    await channel.send(content=content, embed=embed)
    logger.info("Posted message to %s", channel.name)
    return web.Response(status=204)


@routes.post("/post_direct_message")
async def post_direct_message(request):
    """Posts a direct message to a user.

    Format:
        HTTP POST with JSON body

    Args:
        user_id: Discord ID of the channel
        content: message text (Optional)
        embed: embed to add to the message (Optional) (see Discord API documentation for correct format)

    Returns:
        HTTP 204 on success, else raises HTTP exception
    """
    data = await request.json()
    content = data.get("content")
    embed_dict = data.get("embed")
    if "user_id" not in data or (not content and not embed_dict):
        raise web.HTTPBadRequest()
    discord_client = request.app["discord_client"]
    try:
        user = await discord_client.fetch_user(user_id=data["user_id"])
    except NotFound as ex:
        raise web.HTTPNotFound() from ex
    channel = await user.create_dm()
    embed = discord.Embed.from_dict(embed_dict) if embed_dict else None
    await channel.send(content=content, embed=embed)
    logger.info("DM sent to user %s", user.name)
    return web.Response(status=204)
