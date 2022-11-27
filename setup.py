from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="interactions-database",
    version="1.0.0",
    description="Allows for simple disk writing to keep persistant data.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/interactions-py/database",
    author="Axiinyaa",
    author_email="axolpop@outlook.com",
    license="GNU",
    packages=["interactions.ext.database"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    install_requires=["discord-py-interactions", "aiofiles"],
)