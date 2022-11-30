from interactions import CommandContext, ComponentContext, Extension, extension_listener
from json import loads, dumps
from enum import Enum
import aiofiles
import os

class Database(Extension):    
    '''
    The Database Extension.
    '''
    
    i_path = 'interactions/ext/database/databases/'
    
    def __init__(self, client, bot):
        
        t_path = f'{Database.i_path}{bot.me.id}/'
        
        if not os.path.exists(t_path):
            os.mkdir(t_path)
        
        Database.i_path = t_path
    
    class DatabaseType(Enum):
        '''
        Gets the database type.
        '''
        USER = 1
        CHANNEL = 2
        GUILD = 3
        
    async def CreateDatabase(name : str, type : DatabaseType, default_data : dict):
        '''
        Creates a Database if it doesn't already exist. Returns a dictionary object.
        
        Parameters:
            name (str): The name of the database.
            type (Database.DatabaseType): The type of data to check for. This is used as a Primary Key for the database.
            default_data (dict): If a value doesn't exist for the DatabaseType, it adds that value to the database.
        '''
        
        path = f'{Database.i_path}{name}.db'
        
        d_uid = 'interactions_extension_database_UID'
        d_type = 'interactions_extension_database_TYPE'
        d_data = 'interactions_extension_database_DATA'
        
        if not os.path.exists(path):
            
            async with aiofiles.open(path, 'w+') as f:
                default_data.update({d_uid: 0, d_type: type.value})
                default_data.update({d_data: default_data})
                await f.write(dumps(default_data))
            return default_data
    
    async def GetItem(ctx : CommandContext | ComponentContext, database : str):
        '''
        Gets the database using the specified string. Returns a dictionary object.
        
        Parameters:
            ctx (interactions.CommandContext | interactions.ComponentContext): The Context of a command or component.
            database (str): The name of the database to get.
        '''
        
        def get_type(uid):
            '''
            Do not call directly.
            '''
            
            if uid == 1:
                return int(ctx.author.id)
            if uid == 2:
                return int(ctx.channel_id)
            if uid == 3:
                return int(ctx.guild_id)
        
        uid : int = 0
        default_data : dict = {}
        
        db = []
        ids = []
        
        # The only reason why THIS isn't just 'uid' or 'type' is just in-case a user actually does type 'uid' or 'type' into the default_data field.
        d_uid = 'interactions_extension_database_UID'
        d_type = 'interactions_extension_database_TYPE'
        d_data = 'interactions_extension_database_DATA'

        path = f'{Database.i_path}{database}.db'
        
        async with aiofiles.open(path, 'r') as f:
            data_ = await f.read()
            db = data_.split('\n')
            
            uid = get_type(loads(db[0])[d_type])
            default_data = loads(db[0])[d_data]
            
        for slot in db:
            json_data = loads(slot)
            ids.append(json_data[d_uid])
        
        if not uid in ids:
            default_data.update({d_uid: uid})

            str_data = dumps(default_data)
            db.append(str_data)
            
            async with aiofiles.open(path, 'w') as f:
                full_data = '\n'.join(db)
                await f.write(full_data)

            return default_data
        
        index = 0
        for id_ in ids:
            if (uid == id_):
                json_data = loads(db[index])
                return json_data
            index += 1
            
            
    async def SetItem(ctx : CommandContext | ComponentContext, database : str, value : str, data : str):
        '''
        Edits an item within a database. Returns the dictionary object of the edited item.
        
        Parameters:
            ctx (interactions.CommandContext | interactions.ComponentContext): The Context of a command or component.
            database (str): The name of the database to edit.
            value (str): The value in the item to get. For example: {>> "value" <<: "data"}
            data (str): The data in the item to set. For example: {"value": >> "data" <<}
        '''
        
        db = []
        uids = []
        
        uid = 0
        
        def get_type(uid):
            '''
            Do not call directly.
            '''
            
            if uid == 1:
                return int(ctx.author.id)
            if uid == 2:
                return int(ctx.channel_id)
            if uid == 3:
                return int(ctx.guild_id)
        
        d_uid = 'interactions_extension_database_UID'
        d_type = 'interactions_extension_database_TYPE'
        d_data = 'interactions_extension_database_DATA'
        
        path = f'{Database.i_path}{database}.db'
        
        async with aiofiles.open(path, 'r') as f:
            data_ = await f.read()
            db = data_.split('\n')
            uid = get_type(loads(db[0])[d_type])
            default_data = loads(db[0])[d_data]
            
        for slot in db:
            json_data = loads(slot)
            uids.append(json_data[d_uid])
        
        index = 0
        
        json_data = {}
        
        if not uid in uids:
            default_data.update({d_uid: uid})
            
            default_data[value] = data

            str_data = dumps(default_data)
            db.append(str_data)
            
            async with aiofiles.open(path, 'w') as f:
                full_data = '\n'.join(db)
                await f.write(full_data)

            return default_data
        
        for id_ in uids:
            if (uid == id_):
                json_data = loads(db[index])
                json_data[value] = data
                db[index] = dumps(json_data)
            index += 1
            
        async with aiofiles.open(path, 'w') as f:
            full_data = '\n'.join(db)
            await f.write(full_data)
            
        return json_data
    
    async def DeleteItem(ctx : CommandContext | ComponentContext, database : str):
        '''
        Deletes an item within your database. Returns the dictionary of the deleted item, otherwise returns None if an item cannot be found.
        
        Parameters:
            ctx (interactions.CommandContext | interactions.ComponentContext): The Context of a command or component.
            database (str): The name of the database to edit.
        '''
        
        d_uid = 'interactions_extension_database_UID'
        d_type = 'interactions_extension_database_TYPE'
        
        path = f'{Database.i_path}{database}.db'
        
        db = []
        uids = []
        uid = 0
        
        def get_type(uid):
            '''
            Do not call directly.
            '''
            
            if uid == 1:
                return int(ctx.author.id)
            if uid == 2:
                return int(ctx.channel_id)
            if uid == 3:
                return int(ctx.guild_id)
        
        path = f'{Database.i_path}{database}.db'
        
        async with aiofiles.open(path, 'r') as f:
            data_ = await f.read()
            db = data_.split('\n')
            uid = get_type(loads(db[0])[d_type])
            
        for slot in db:
            json_data = loads(slot)
            uids.append(json_data[d_uid])
            
        if not uid in uids:
            return None
        
        database_ = {}
        
        i = 0
        for id_ in uids:
            if id_ == uid:
                database_ = db.pop(i)
                
                async with aiofiles.open(path, 'w') as f:
                    full_data = '\n'.join(db)
                    await f.write(full_data)
                
                return database_
            
            i += 1