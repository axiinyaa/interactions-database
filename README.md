# interactions-database
A simple json database writer for interactions-py that allows for simple persistence.

## Doesn't Persistence or wait-for exist?
Persistence, wait-for and Database all have their own use cases. For example, Persistence and wait-for does NOT write to disk, while Database does. This library isn't designed to compete with either of those libraries, and is more focused on storing data quickly to be used at any time.

## How do I use it?
First, install the extension using this command.
```
pip install git+https://github.com/Axiinyaa/interactions-database
```

Once installed, import the module like so.

```py
import interactions
from interactions.ext.database import Database

bot = interactions.Client(...)

bot.load('interactions.ext.database')
```

Then, to create a database, use ``Database.CreateDatabase()``. It's highly recommended to do this during ``on_start()``.
```py
import interactions
from interactions.ext.database import Database

bot = interactions.Client(...)

bot.load('interactions.ext.database')

@bot.event()
async def on_start()

    default_data = {"amount_of_coins" : 0}

    await Database.CreateDatabase(
            name = 'coins',
            type = Database.DatabaseType.USER,
            default_data = default_data
        )
```

To get data from the database, use ``Database.GetItem()``, to set data, use ``Database.SetItem()``.

```py

# Getting the Database called 'coins'
db = await Database.GetItem(ctx = ctx, database = 'coins')

# Grabbing a value from the database. This a dictionary so it's recommended to use the get() function.
coins = db.get('amount_of_coins', 0)

# Setting the amount_of_coins value in the 'coins' database.
await Database.SetItem(ctx = ctx, database = 'coins', value = 'amount_of_coins', data = coins + 1)

await ctx.send('Added one coin!')
```

To delete an item from the database, use ``Database.DeleteItem()``

```py

db = await Database.DeleteItem(ctx = ctx, database = 'coins')

coins = db.get('amount_of_coins', 0)

await ctx.send(f'Successfully got rid of all your coins. You had {coins} amount of coins!`)

```

## Performance Concerns?
While performance isn't significantly important for discord bots, this will write to a file and will loop through it to find values, meaning it will have a O(n) time complexitivity. This means that this extension isn't recommended for HUGE databases, use an actual database instead in those cases!
