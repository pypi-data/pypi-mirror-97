from setuptools import setup

version = "0.0.8"

with open("README.md", "r") as f:
	long_desc = f.read()

setup(
name="discord-ext-bot",
author="Alex Hutz",
author_email="frostiiflames@gmail.com",
url="https://github.com/FrostiiWeeb/discord-ext-bot",
version=version,
packages=["discord.ext.bot"],
license='MIT',
long_description=long_desc,
long_description_content_type="text/markdown",
description="An package for discord.py.",
install_requires=['discord.py>=1.5.1', 'jishaku'],
python_requires='>=3.8.1'
)