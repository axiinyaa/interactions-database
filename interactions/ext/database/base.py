"The base of the extension."

from interactions.ext import Base, Version, VersionAuthor
from .database import Database

version = Version(
    version="1.0.0",
    author=VersionAuthor(
        name="Axiinyaa",
        email="axolpop@outlook.com",
    ),
)

base = Base(
    name="Database",
    version=version,
    link="",
    description="An extension to add simple databases.",
    packages="interactions.ext.database",
)

def setup(client, uid = 'database'):
    return Database(client, uid)