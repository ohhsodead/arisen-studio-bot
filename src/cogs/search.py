"""
Cog module for the search command.
"""

from typing import Any

import aiohttp
import discord
from discord.ext import commands, pages

from src.utils.config import Config


class Search(commands.Cog):
    """
    Cog class for the search command.
    """

    search = discord.SlashCommandGroup("search", "Search for something in the categories.")

    def __init__(self, client: discord.AutoShardedBot) -> None:
        self.client = client

    async def search_json_file(self, url: str, query: str) -> list:
        """
        Search the json file for the query.

        :param url: The url of the file.
        :type url: str
        :param query: The query to search for.
        :type query: str

        :return: The list of objects.
        :rtype: list
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                result = await response.json(content_type="text/plain")
                return [key for key in result["Mods"] if query.lower() in key["Name"].lower() or query.lower() in key["Description"].lower()]

    async def get_game_name(self, category_id: str) -> str:
        """
        Get the game name from the category id.

        :param category_id: The category id.
        :type category_id: str

        :return: The game name.
        :rtype: str
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("https://raw.githubusercontent.com/ohhsodead/arisen-studio-database/main/categories.json") as resp:
                result = await resp.json(content_type="text/plain")
                return next((i["Title"] for i in result["Categories"] if i["Id"] == category_id), "Unknown Game")

    @search.command(description="Search in the categories for PlayStation 3")
    @discord.option(
        name="category",
        description="The category to search in.",
        required=True,
        choices=[discord.OptionChoice(name=k, value=v) for k,v in {"Game Mods": "gamemods", "Homebrew": "homebrew"}.items()],
    )
    @discord.option(name="query", description="The query to search for.", required=True)
    async def ps3(self, ctx: discord.ApplicationContext, category: str, query: str) -> Any:
        """
        The command for searching the ps3 files.
        """
        await ctx.defer(ephemeral=True)
        if ctx.channel.id != Config.ps3:
            return await ctx.respond("This command can only be used in the #search channel.")
        url = (
            "https://raw.githubusercontent.com/ohhsodead/arisen-studio-database/main/PS3/game-mods.json"
            if category == "gamemods"
            else "https://raw.githubusercontent.com/ohhsodead/arisen-studio-database/main/PS3/homebrew.json"
        )
        data = await self.search_json_file(url, query)
        if not data:
            return await ctx.respond(f"No result(s) found for {query} in {category}")

        pgs = [
            discord.Embed(
                title=await self.get_game_name(result["CategoryId"]),
                description=result['Name'],
                color=Config.embed_color,
            ).set_footer(text=f"Search Results ({key+1}/{len(data)})").add_field(name="Platform", value=result["Platform"]).add_field(name="Created By", value=result["CreatedBy"]).add_field(name="Submitted By", value=result["SubmittedBy"]).add_field(name="Version", value=result["Version"]).add_field(name="Game Mode", value=result["GameMode"]).add_field(name="Mod Type", value=result["ModType"]).add_field(name="Description", value=result["Description"][:1024], inline=False).add_field(name="Download Files", value="\n".join([f"[{i['Name']} ({i['Version']})]({i['Url']})\n" for i in result['DownloadFiles']]))
            for key, result in enumerate(data)
        ]

        paginator = pages.Paginator(pages=pgs)
        await paginator.respond(ctx.interaction, ephemeral=True)

    @search.command(description="Search in the categories for Xbox 360")
    @discord.option(
        name="category",
        description="The category to search in.",
        required=True,
        choices=[discord.OptionChoice(name=k, value=v) for k,v in {"Plugins": "plugins"}.items()],
    )
    @discord.option(name="query", description="The query to search for.", required=True)
    async def xbox360(self, ctx: discord.ApplicationContext, category: str, query: str) -> Any:
        """
        The command for searching the xbox360 files.
        """
        await ctx.defer(ephemeral=True)
        if ctx.channel.id != Config.xbox360:
            return await ctx.respond("This command can only be used in the #search channel.")
        url = "https://raw.githubusercontent.com/ohhsodead/arisen-studio-database/main/XBOX360/plugins.json"
        data = await self.search_json_file(url, query)
        if not data:
            return await ctx.respond(f"No result(s) found for {query} in {category}")

        pgs = [
            discord.Embed(
                title=await self.get_game_name(result["CategoryId"]),
                description=result['Name'],
                color=Config.embed_color,
            ).set_footer(text=f"Search Results ({key+1}/{len(data)})").add_field(name="Platform", value=result["Platform"]).add_field(name="Created By", value=result["CreatedBy"]).add_field(name="Submitted By", value=result["SubmittedBy"]).add_field(name="Version", value=result["Version"]).add_field(name="Game Mode", value=result["GameMode"]).add_field(name="Mod Type", value=result["ModType"]).add_field(name="Description", value=result["Description"][:1024], inline=False).add_field(name="Download Files", value="\n".join([f"[{i['Name']} ({i['Version']})]({i['Url']})\n" for i in result['DownloadFiles']]))
            for key, result in enumerate(data)
        ]

        paginator = pages.Paginator(pages=pgs)
        await paginator.respond(ctx.interaction, ephemeral=True)


def setup(client: discord.AutoShardedBot) -> None:
    """
    The setup function for cog
    """
    client.add_cog(Search(client))
