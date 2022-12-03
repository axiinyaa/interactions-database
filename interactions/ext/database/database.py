from interactions import CommandContext, ComponentContext, Extension, extension_listener
from json import loads, dumps
from enum import Enum
from typing import Union

import aiofiles
import os
class Database(Extension):    
    '''
    The Database Extension.
    '''
    
    i_path = 'interaction-database/'
    
    class DatabaseType(Enum):
        '''
        Gets the database type.
        '''
        USER = 1
        CHANNEL = 2
        GUILD = 3
    
    @staticmethod
    async def create_database(name : str, type : DatabaseType, default_data : dict):
        '''
        Creates a Database if it doesn't already exist.
        
        :param name: The name of the database.
        :type name: str
        :param type: The type of database to create.
        :type type: database.Database.DatabaseType
        :param default_data: The default data to fall back to whenever an item doesn't exist yet.
        :type default_data: dict
        :return: Dictionary
        :rtype: dict
        '''
        
        path = f'{Database.i_path}{name}.db'
        
        d_uid = 'interactions_extension_database_UID'
        d_type = 'interactions_extension_database_TYPE'
        
        if not os.path.exists(path):
            
            if not os.path.exists(Database.i_path):
                os.mkdir(Database.i_path)
            
            f = await aiofiles.open(path, 'x')
            default_data.update({d_uid: 0, d_type: type.value})
            await f.write(dumps(default_data))
            await f.close()
            return default_data
    
    @staticmethod
    async def get_item(ctx : Union[CommandContext, ComponentContext], database : str):
        '''
        Gets the database using the specified string.
        
        :param ctx: The context of a command or component.
        :type ctx: Union[interactions.CommandContext, interactions.ComponentContext]
        :param database: The database to get an item from.
        :type database: str
        :return: Dictionary
        :rtype: dict
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
        
        d_data = ''

        path = f'{Database.i_path}{database}.db'
        
        async with aiofiles.open(path, 'r') as f:
            data_ = await f.read()
            db = data_.split('\n')
            
            uid = get_type(loads(db[0])[d_type])
            default_data = loads(db[0])
            
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
            
    @staticmethod      
    async def set_item(ctx : Union[CommandContext, ComponentContext], database : str, value : str, data : Union[str, CommandContext]):
        '''
        Edits an item within a database.
        
        :param ctx: The context of a command or component.
        :type ctx: Union[interactions.CommandContext, interactions.ComponentContext]
        :param database: The database to edit an item.
        :type database: str
        :param value: The value to edit from the item.
        :type value: str
        :param data: The data to edit from the value.
        :type data: Union[str, CommandContext]
        :return: A dictionary of the edited item.
        :rtype: dict
        '''
        
        if type(data) == CommandContext:
            data = data._json
        
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
        
        path = f'{Database.i_path}{database}.db'
        
        async with aiofiles.open(path, 'r') as f:
            data_ = await f.read()
            db = data_.split('\n')
            uid = get_type(loads(db[0])[d_type])
            default_data = loads(db[0])
            
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
    
    @staticmethod
    async def delete_item(ctx : Union[CommandContext, ComponentContext], database : str):
        '''
        Deletes an item within your database.
        
        :param ctx: The context of a command or component.
        :type ctx: Union[interactions.CommandContext, interactions.ComponentContext]
        :param database: The database to delete an item from.
        :type database: str
        :return: A dictionary of the deleted item, returns None if no item was found.
        :rtype: Union[dict, None]
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