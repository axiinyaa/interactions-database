from interactions import *

async def convert_to_json(data : CommandContext):
    json_data = data._json
    
    print(json_data)