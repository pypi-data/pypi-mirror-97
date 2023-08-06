import asyncio
import re
from inspect import signature
import logging
import asyncio
import discord
from discord.ext import commands
from typing import Union
import os

__all__ = ["Bot"]

__version__ = "0.0.7"

class BaseBot(commands.Bot):
	def __init__(self, *args, **kwargs):
		super().__init__(allowed_mentions=discord.AllowedMentions(users=True, everyone=False, replied_user=False, roles=False), *args, **kwargs)	

class Bot(BaseBot):
	"""
	A pre-made bot with extensions like Jishaku, etc..
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.cog_list = [f"cogs.{cog[:-3]}" for cog in os.listdir("./cogs")] + ["jishaku"]
	
	async def on_ready(self):
		for ext in self.cog_list:
			self.load_extension(ext)
		print(f"{'-' * 20}\nID: {self.userr.id}\nName: {self.user}")		