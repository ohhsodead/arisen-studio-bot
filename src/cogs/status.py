"""
Cog module for the status command.
"""

from typing import Any

import aiohttp
import discord
from discord.ext import commands, pages

from src.utils.config import Config


class Status(commands.Cog):
    """
    Cog class for the status command.
    """

    def __init__(self, client: discord.AutoShardedBot) -> None:
        self.client = client

    @discord.slash_command(description="Get the status of Arisen services.")
    async def status(self, ctx: discord.ApplicationContext) -> Any:
        """
        The command for checking the status of the websites.
        """
        await ctx.defer()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.githubstatus.com/api/v2/status.json") as resp:
                if resp.status != 200:
                    github_status = "🔴  GitHub - Down"
                else:
                    try:
                        json = await resp.json()
                        if json["status"]["description"] == "All Systems Operational":
                            github_status = "🟢  GitHub - Fully Operational"
                        else:
                            github_status = "🟡  GitHub - Partly Operational"
                    except Exception:
                        github_status = "🔴  GitHub - Down"
            async with session.get("https://status.dropbox.com/api/v2/status.json") as resp:
                if resp.status != 200:
                    dropbox_status = "🔴  Database - Down"
                else:
                    try:
                        json = await resp.json()
                        if json["status"]["description"] == "All Systems Operational":
                            dropbox_status = "🟢  Database - Fully Operational"
                        else:
                            dropbox_status = "🟡  Database - Partly Operational"
                    except Exception:
                        dropbox_status = "🔴  Database - Down"
            async with session.get("https://arisen.studio/") as resp:
                if resp.status != 200:
                    arisen_status = "🔴  Website - Down"
                else:
                    arisen_status = "🟢  Website - Fully Operational"
            async with session.get("https://arisenstudio.app/") as resp:
                if resp.status != 200:
                    arisenapp_status = "🔴  Web Store - Down"
                else:
                    arisenapp_status = "🟢  Web Store - Fully Operational"
        embed = discord.Embed(
            title="Current Status",
            description=f"{github_status}\n{dropbox_status}\n{arisen_status}\n{arisenapp_status}",
            color=Config.embed_color,
        )
        await ctx.respond(embed=embed)

    @discord.slash_command(description="Get the status of Arisen services.")
    async def hi(self, ctx: discord.ApplicationContext) -> Any:
        await ctx.respond("hello")

    @discord.slash_command(description="Get ")
    async def hiii(self, ctx: discord.ApplicationContext) -> Any:
        await ctx.respond("hellogghghg")


def setup(client: discord.AutoShardedBot) -> None:
    """
    The setup function for cog
    """
    client.add_cog(Status(client))
