#this file is for continuosuly sending the username data through websockets to the html "index.html"

import websockets
import asyncio
import os
username = " "

async def server(websocket,path):
    global username
    async for message in websocket:
        with open("details.txt", "r") as f:
            details = f.read().strip()
            #print("username")
            #print(username)
            
        await websocket.send(details)
            
start_server = websockets.serve(server,'localhost',5555)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()