from datetime import *
import discord
from discord.ext import commands
import asyncio
import random

from bot import Bot

class CommandBot:
    def __init__(self, id, command, help):
        self.id = id
        self.command = command
        self.help = help

        self.name = client.get_server(id)
    #def setId(self,id)
    #    self.id = id
bot = commands.Bot(command_prefix='botfix', description='my first bot buddy')
client = discord.Client()
tropServerID = 380071150950285312
global allSeeing# =CommandBot(0,"+","help")
global tBone# =CommandBot("380071150950285312","!","commands")
global econ# = CommandBot("268122068007124993","$","econ")
global ready
ready = False

gameList = [[], []]
global overRide
overRide = False

async def getPlayer(id):#returns player location or -1
    gameList = await loadData()
    for i in range(len(gameList)):
        #print(gameList[i][0]+' '+ id)
        if str(gameList[i][0]) == id:
            return i
    return -1

async def populatePoints():
    tropServer = client.get_server(str(tropServerID))
    memberList = tropServer.members
    printStr = ""
    idList = []
    pointList = []
    for member in memberList:
        if not member.bot:
            idList.append(member.id)
            pointList.append(0)
    await saveData(idList, pointList)

@client.event
async def on_ready():
    global ready
    ready = True
    print('Bot ' + client.user.name + ' is activated')
    gameList = await loadData()
    #print(gameList)

    global allSeeing #=CommandBot(0,"+","help")
    global tBone #=CommandBot("380071150950285312","!","commands")
    global econ #= CommandBot("268122068007124993","$","econ")
    allSeeing = CommandBot(client.user.id, "+", "help")
    tBone = CommandBot("451141489771151368", "!", "commands")
    econ = CommandBot("454322901462548482", "$", "econ")

@bot.command(pass_context=True)
@asyncio.coroutine
def info(ctx):
    server = ctx.message.author.server
    server_name = server.name
    server_id = server.id
    server_owner = server.owner.name

    print("server name: {}"
          "server id: {}"
          "server owner: {}"
          .format(server_name, server_id, server_owner))

@client.event
async def on_message(message):
    global overRide
    global allSeeing
    global tBone
    global econ
    print("global" + str(overRide))
    if not message.author.bot:
        if message.content.startswith(allSeeing.command, 0, len(allSeeing.command)):
            success = False
            command = message.content[len(allSeeing.command):]
            #server commands
            if message.server:
                if command.startswith('test'):
                    if message.server.id == str(tropServerID):
                        success = True
                        print(True)
                    else:
                        print(message.server.id + ' != ' + str(tropServerID))
                        success = True
                    await client.send_message(message.channel, 'Passed Test')
                elif command.startswith('score'):
                    success = True
                    gameList = await loadData()
                    check = await getPlayer(message.author.id)
                    if check != -1:
                        points = str(gameList[check][1])
                        await client.send_message(message.channel, '<@!' + message.author.id + '> has ' + points + ' points')
                    else:
                        print('user ' + message.author.id + 'does not exist')
                elif command.startswith('override'):
                    for role in message.author.roles:
                        if role.name == 'mod':
                            print("Local " + str(overRide))
                            if overRide:
                                overRide = False
                            else:
                                overRide = True
                        success = True
                elif command.startswith('name'):
                    success = True
                    await client.send_message(message.channel,message.author.nick + ', A new name will cost 500 points.')
                    gameList = await loadData()
                    check = await getPlayer(message.author.id)
                    if check != -1 and gameList[check][1] >= 500:
                        await client.send_message(message.channel,'+c or +confirm / +d or +deny')
                    else:
                        await client.send_message(message.channel,'you need ' + str(500 - gameList[check][1]) + ' Points :(')
                elif command.startswith('c') or command.startswith('confirm'):
                    i = 0
                    savedMessage = message
                    savedMessage.content = ""
                    payed = True
                    async for mes in client.logs_from(message.channel,3):
                        if i == 0:#user
                            #print("mess1: "+mes.content)
                            savedMessage = mes
                        elif i == 1 and mes.content.startswith('you'):
                            payed = False
                        elif i == 2 and mes.author.id == client.user.id and payed:#bot
                            #print("mess2: "+mes.content)
                            name = mes.author.id
                            #print(savedMessage.content+" <- content")
                            if mes.content.startswith(savedMessage.author.nick):
                                gameList = await loadData()
                                check = await getPlayer(message.author.id)
                                if check != -1:
                                    gameList[check][1]-=500
                                    await saveData(gameList)
                                newname = await getRandomName()
                                await client.change_nickname(message.author,newname)
                                await client.send_message(message.channel,message.author.name + ' will now be known as ' + newname)
                            elif savedMessage.content != "":
                                #print(savedMessage.content + ' != <@!' + name
                                #+'>')
                                print("Error: invalid user id, cannot buy name")
                            elif payed == False:
                                print("Cannot pay")
                            else:
                                print("savedMessage was not set")
                        i+= 1
                elif command.startswith('+d') or command.startswith('+deny'):
                    donothing = true#todo clear shopping
            #server and non server
            if command.startswith('sleep'):
                success = False
                await client.delete_message(message)
                previous = await client.send_message(message.channel, 'Good Night')
                await asyncio.sleep(5)
                await client.edit_message(previous, 'Done sleeping')
            elif command.startswith('time'):
                await client.send_message(message.channel, "the time is currently " + str(datetime.now())[11:-7])
            elif command.startswith('help'):
                success = True
                await help(message.channel)
            if success:
                await client.delete_message(message)
    #Bot only messages
    #bot only server commands
    elif message.content.startswith(allSeeing.command, 0, len(allSeeing.command)) and message.server:
        print("bot entered command on server")
        success = True
        command = message.content[len(allSeeing.command):]
        if command.startswith('help'):
            print("help command")
            await help(message.channel)

        if success:
            await client.delete_message(message)
    #bot counter
    elif message.content[0:len('Bot has counted')] == 'Bot has counted' and overRide:
        #success =True

        i = 0
        userid = ""
        async for message in client.logs_from(message.channel, 2):
            if i == 1:
                userid = message.author.id
            elif message.author.id == str(tBone.id):
                pointAdd = int(message.content[len('Bot has counted '):-len(' times')])
            i+= 1
        gameList = await loadData()
        check = await getPlayer(userid)
        print(check)
        if check != -1:
            gameList[check][1] += pointAdd
        await saveData(gameList)
    #override all bot commands
    elif client.user.id != message.author.id and overRide:
        content = message.content
        await client.delete_message(message)
        message.content = message.author.name + ":\n" + content
        await client.send_message(message.channel, message.content)


async def loopTask():
    sleep = 10
    global ready
    await client.wait_until_ready()
    while not client.is_closed:
        if ready:
            sleep = 60
            tropServer = client.get_server(str(tropServerID))
            for channel in tropServer.channels:
                if channel.name == "news-update":
                    async for message in client.logs_from(channel, 5):
                        if len(message.reactions) != 0:
                            for reaction in message.reactions:
                                if  reaction.emoji == "🆕" and reaction.count > 1:
                                    for reaction in message.reactions:
                                        if reaction.emoji == "🆕":
                                            message.reactions = ["🆕"]#reset reactions

                                    if message.author.id == allSeeing.id:
                                        await client.delete_message(message)
                                        newmessage = await client.send_message(channel, allSeeing.command + allSeeing.help)
                                        await client.add_reaction(newmessage,"🆕")
                                    elif message.author.id == tBone.id:
                                        await client.delete_message(message)
                                        newmessage = await  client.send_message(channel, tBone.command + tBone.help)
                                        await client.add_reaction(newmessage,"🆕")
                                    elif message.author.id == econ.id:
                                        await client.delete_message(message)
                                        newmessage = await  client.send_message(channel, econ.command + econ.help)
                                        await client.add_reaction(newmessage,"🆕")
                        else:
                            if message.author.id == allSeeing.id:
                                await client.add_reaction(message,"🆕")
                            elif message.author.id == tBone.id:
                                await client.add_reaction(message,"🆕")
                            elif message.author.id == econ.id:
                                await client.add_reaction(message,"🆕")
                            
        await asyncio.sleep(sleep) # task runs every 15 minutes
async def help(channel):
    #discord.Embed(title="Commands", description="This is the list of
    #commands", color=0xff0055)
    await client.send_message(channel,"""```
AllSeeingEye - Commands
*commands start with "+"
Admin Commands:
-   override| AllSeeingEye is watching
Server Commands:
-   score   | displays your score
-   top     | displays top score
-   name    | trade points for a new name, needs conformation   
Local Commands:
-   help    | shows this list
-   sleep   | responds after 5 seconds
```""")

async def saveData(gameList):
    file = open("TropicalServer.txt","w")
    #memberList =
    i = 0
    for id in gameList:
        file.write(str(id[0]) + "," + str(id[1]) + '\n')
        i+=1
    file.close()

#async def saveData(str):
#    file = open("TropicalServer.txt","w")
#    #memberList =
#    #for member in
#    file.write(str)
#    file.close()
async def loadData():
    idpointList = []
    file = open("TropicalServer.txt","r")
    fileList = file.readlines()
    for line in fileList:
        idpointList.append(line.split(','))
        idpointList[-1][1] = int(idpointList[-1][-1])
        #print(idpointList[-1][1])
    return idpointList

async def getRandomName():
    random.seed()
    file = open("NamesList.txt","r")
    fileList = file.readlines()
    randname = random.randint(0,len(fileList) - 1)
    return fileList[randname]

readfile = ""
with open("secrets.txt","r") as filereader:
    readfile = filereader.readline()
    pass

client.loop.create_task(loopTask())
client.run(readfile)
print("Bot Deactivated")
