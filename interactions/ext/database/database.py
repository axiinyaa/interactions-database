from interactions import CommandContext, ComponentContext, Extension, extension_listener
from json import loads, dumps
from enum import Enum
import aiofiles
import os

class Database(Extension):    
    '''
    The Database Extension.
    '''
    
    @extension_listener()
    async def on_start(self):
        
        global i_path
        
        t_path = f'{i_path}{self.client.me.id}/'
        
        if not os.path.exists(t_path):
            os.mkdir(t_path)
            i_path = t_path
            
            print(i_path)
    
    class DatabaseType(Enum):
        '''
        Gets the database type.
        '''
        USER = 1
        CHANNEL = 2
        GUILD = 3
    
    async def GetDatabase(ctx : CommandContext | ComponentContext, type : DatabaseType, database : str, default_data : dict):
        '''
        Gets the database using the specified string. If the database doesn't exist, it creates it instead.
        
        Parameters:
            ctx (interactions.CommandContext | interactions.ComponentContext): The Context of a command or component.
            type (database.DatabaseType): The type of data to check for. This is used as a Primary Key for the database.
            database (str): The name of the database to use.
            default_data (dict): If a value doesn't exist for the DatabaseType, it adds that value to the database.
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
        
        uid = get_type(type.value)
        
        db = []
        ids = []
        
        path = f'{i_path}{database}.db'
        
        # The only reason why THIS isn't just 'uid' or 'type' is just in-case a user actually does type 'uid' or 'type' into the default_data field.
        d_uid = 'interactions_extension_database_UID'
        d_type = 'interactions_extension_database_TYPE'
            
        if not os.path.exists(path):
            
            async with aiofiles.open(path, 'w+') as f:
                default_data.update({d_uid: uid, d_type: type.value})
                await f.write(dumps(default_data))
            return default_data
        
        async with aiofiles.open(path, 'r') as f:
            data_ = await f.read()
            print(data_)
            db = data_.split('\n')
            
            uid = get_type(loads(db[0])[d_type])
            
        for slot in db:
            json_data = loads(slot)
            ids.append(json_data[d_uid])
        
        if not uid in ids:
            default_data.update({d_uid: uid, d_type: type.value})

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
            
            
    async def SetDatabase(ctx : CommandContext | ComponentContext, database : str, value : str, data : str):
        '''
        Sets a value async within an EXISTING database. It's recommended to call GetDatabase(...) first before calling this.
        
        Parameters:
            ctx (interactions.CommandContext | interactions.ComponentContext): The Context of a command or component.
            database (str): The name of the database to use.
            value (str): The value in the database to get. For example: {>> "value" <<: "data"}
            data (str): The data in the database to set. For example: {"value": >> "data" <<}
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
        
        path = f'{i_path}{database}.db'
        
        async with aiofiles.open(path, 'r') as f:
            data_ = await f.read()
            db = data_.split('\n')
            uid = get_type(loads(db[0])[d_type])
            
        for slot in db:
            json_data = loads(slot)
            uids.append(json_data[d_uid])
        
        index = 0
        
        json_data = {}
        
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