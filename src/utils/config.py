"""
Config module for the bot.
"""

import yaml


class Config:
    """
    Config class for the bot.
    """

    with open("config.yml", "r") as f:
        _raw_config = yaml.safe_load(f)

    embed_color = _raw_config["embed-color"]

    ps3 = _raw_config["ps3"]
    xbox360 = _raw_config["xbox360"]
