"""
Cog module for the message and api command.
"""

from typing import Any

import discord
from discord.ext import commands, pages
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from src.utils.config import Config


class Message(commands.Cog):
    """
    Cog class for the status command.
    """

    def __init__(self, client: discord.AutoShardedBot) -> None:
        self.client = client

    @discord.slash_command(description="Get the status of Playstation services.")
    async def pstatus(self, ctx: discord.ApplicationContext) -> Any:
        await ctx.defer()
        """
        The command for checking the status of the websites.
        """
        # URL of the page we want to scrape
        url = "https://status.playstation.com/#statusArea"

        # Initiating the webdriver.
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode
        driver = webdriver.Chrome(options=options)

        driver.get(url)

        # This is just to ensure that the page is loaded
        time.sleep(3)

        html = driver.page_source

        #This renders the JS code and stores all
        # of the information in static HTML code.

        # Now, we could simply apply bs4 to the html variable
        soup = BeautifulSoup(html, "html.parser")
        all_divs = soup.find('div', {'id' : 'statusArea'})
        main_service = all_divs.find('span', class_='offscreen').get_text()
        if "up" in main_service:
         embed = discord.Embed(
            title="Playstation Status",
            description=f"🟢 ✦ {main_service}",
            color=Config.embed_color,
         )
         await ctx.respond(embed=embed)
        else:
           embed = discord.Embed(
            title="Playstation Status",
            description=f"🔴 ✦ {main_service}",
            color=Config.embed_color,
           )
           await ctx.respond(embed=embed)
        driver.quit()

    @discord.slash_command(description="Get the status of Xbox services.")
    async def xstatus(self, ctx: discord.ApplicationContext) -> Any:
        await ctx.defer()
        """
        The command for checking the status of the websites.
        """
        # URL of the page we want to scrape
        url = "https://support.xbox.com/en-GB/xbox-live-status"

        # Initiating the webdriver.
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode
        driver = webdriver.Chrome(options=options)

        driver.get(url)

        # This is just to ensure that the page is loaded
        time.sleep(15)

        html = driver.page_source

        #This renders the JS code and stores all
        # of the information in static HTML code.

        # Now, we could simply apply bs4 to the html variable
        soup = BeautifulSoup(html, "html.parser")
        all_divs = soup.find('div', {'id': 'root'})
        div_status = all_divs.find('div', class_="ms-Stack css-141")
        if div_status:
          first_span = div_status.find('span')
          if first_span:
            main_service = first_span.get_text()
            if "up" in main_service:
              embed = discord.Embed(
               title="Xbox Status",
               description=f"🟢 ✦ {main_service}",
               color=Config.embed_color,
              )
              await ctx.respond(embed=embed)
            else:
              embed = discord.Embed(
               title="Xbox Status",
               description=f"🔴 ✦ {main_service}",
               color=Config.embed_color,
              )
              await ctx.respond(embed=embed)
        driver.quit()

    @discord.slash_command(description="Send a message to a specific channel.")
    async def send(self, ctx: discord.ApplicationContext, message: str, channel: discord.TextChannel):
        if ctx.author.id != 212676144934289408:
            await ctx.respond("You are not authorized to use this command.", delete_after=5)
            return
        else: 
           await ctx.respond('Message Sent Successfully', delete_after=5)

        await channel.send(message)

        
    
def setup(client: discord.AutoShardedBot) -> None:
    """
    The setup function for cog
    """
    client.add_cog(Message(client))