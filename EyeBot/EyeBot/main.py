import asyncio
from bot import *

#Global Varibles
global ready
ready = False
global botty

#Start client
client =discord.Client()

#Activate Bot
@client.event
async def on_ready():
    global ready
    global botty
    ready = True

    print('User: '+ client.user.name+' is online')

    botty = Bot(client,"380071150950285312",{"ID":"","Type":""},"-",
        "EyeSee2",
        "Custom Bot implimentation for easy command customization"
        )

    #paginator =commands.Paginator.add_line("this is my line")
    pass

@client.event
async def on_message(message):
    global botty
    await botty.on_message(message)
    pass

#endless loop
async def loopTask():
    sleep = 10
    global ready
    global botty
    await client.wait_until_ready()
    while not client.is_closed:
        if ready:
            sleep = 60           
        await asyncio.sleep(sleep) # task runs every 15 minutes
    pass

#read Bot API Key
readfile =""
with open("secrets.txt","r") as filereader:
    readfile = filereader.readline()
    pass

#End of file
client.loop.create_task(loopTask())
client.run(readfile)
print("Bot Deactivated")