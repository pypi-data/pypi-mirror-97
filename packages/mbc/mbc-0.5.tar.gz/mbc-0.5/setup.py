from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='mbc',
    version='0.5',
    description='Wrapper for the moonlist api',
    long_description="Package was renamed to [moonlistclient](https://pypi.org/project/moonlistclient)",
    long_description_content_type="text/markdown",
    packages=['moonlistclient'],
    author_email='zyzel19@gmail.com',
    url="https://github.com/VadyChel/MoonlistClient",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pydantic",
        "discord.py",
        "aiohttp"
    ]
)