import asyncio
import re
from inspect import signature
import logging
import asyncio
import discord
from discord.ext import commands
from typing import Union
import os
from pathlib import Path

cwd = Path(__file__).parents[0]
cwd = str(cwd)

__all__ = ["Bot"]

__version__ = "0.0.9"

class BaseBot(commands.Bot):
	def __init__(self, *args, **kwargs):
		super().__init__(allowed_mentions=discord.AllowedMentions(users=True, everyone=False, replied_user=False, roles=False), *args, **kwargs)	

class Bot(BaseBot):
	"""
	A pre-made bot with extensions like Jishaku, etc..
	"""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.cog_list = ["cogs.fun", "cogs.misc", "jishaku"]
	
	async def on_ready(self):
		for ext in self.cog_list:
			self.load_extension(ext)
		print(f"{'-' * 20}\nID: {self.userr.id}\nName: {self.user}")		