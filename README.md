# interactions-database
A simple json database writer for interactions-py that allows for simple persistence.

## Doesn't Persistence or wait-for exist?
Persistence, wait-for and Database all have their own use cases. For example, Persistence and wait-for does NOT write to disk, while Database does. This library isn't designed to compete with either of those libraries, and is more focused on storing data quickly to be used at any time.

## How do I use it?
It's quite simple.

First, import the module like so:
```py
import interactions
from interactions.ext.database import Database

bot = interactions.Client(...)

bot.load('interactions.ext.database')
```

Now, you need to create a dictionary to fall back to whenever there is no data for a channel, user or guild.
```py
import interactions
from interactions.ext.database import Database

bot = interactions.Client(...)

bot.load('interactions.ext.database')

@bot.command()
async def add_one_coin(ctx : interactions.CommandContext)

    default_data = {"amount_of_coins" : 0}
```

Next, it's time to create the database. Use ``Database.GetDatabase()`` to create one. If it already exists, it simply just grabs it.
```py
import interactions
from interactions.ext.database import Database

bot = interactions.Client(...)

bot.load('interactions.ext.database')

@bot.command()
async def add_one_coin(ctx : interactions.CommandContext)

    default_data = {"amount_of_coins" : 0}

    db = Database.GetDatabase(
            ctx = ctx,
            type = Database.DatabaseType.USER,
            database = 'coins',
            default_data = default_data
        )
```

To set data for the database, use ``Database.SetDatabase()``.

```py
# Default Data to fall back to.
default_data = {"amount_of_coins" : 0}

# Creating/Getting the Database called 'coins'
db = Database.GetDatabase(
        ctx = ctx,
        type = Database.DatabaseType.USER,
        database = 'coins',
        default_data = default_data
    )

# Grabbing a value from the database. This a dictionary so it's recommended to use the get() function.
coins = db.get('amount_of_coins', 0)

# Setting the amount_of_coins value in the 'coins' database.
Database.SetDatabase(
    ctx = ctx,
    database = 'coins',
    value = 'amount_of_coins',
    data = coins += 1
)

await ctx.send('Added one coin!')
```

## Performance Concerns?
While performance isn't significantly important for discord bots, this will write to a file and will loop through it to find values, meaning it will have a O(n) time complexitivity. This means that this extension isn't recommended for HUGE databases, use an actual database instead in those cases!