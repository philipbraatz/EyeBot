import discord
from discord.ext import commands
from Command import *

global isReady
isReady =False

class Bot(object):

    ready =False

    client =""
    
    key =""

    server = ""
    channelList =[]#{"ID":"","Type":""}

    commandList =[]
    def getCommands(self):
        return self.commandList

    curMessage={"Command":"","Desc":"","Priv":""}


    previousMessage=""

    title =""
    desc =""
    def __init__(self,client, serverID, channelSet, key,title,desc):
        self.client =client
        self.server =serverID
        self.channelList =channelSet
        self.key = key
        
        self.commandList =[
            command(self,"help","shows this list","ALL","Commands\\Default.py"),
            command(self,".","Bot cannot see messages that start with .","ALL",""),
            command(self,"ping","Check if bot is responding","ALL","Commands\\Default.py"),
            command(self,"add","adds 2 numbers","ALL","Commands\\Default.py"),
            ]

        self.title =title
        self.desc =desc
        pass


    def addCommand(self,command):#command is dict with command and description and privledge
        if type(command) =="dict":
            if "command" in command and "Desc" and "Priv" in command:
                return _checkcommand(self,command)
        elif type(command) =="list":
            for c in command:
                addCommand(c)
        else:
            return False

    def _checkcommand(self,command):#command is dict with command and description
        if( len(command["Command"]) !=0 and 
           type(command["Command"]) == "str" and 
           type(command["Desc"]) == "str" and
            type(command["Priv"]) == "str"
           ):
            if command["Priv"] =="":
                command["Priv"] = "ALL"
            if command[command].find(' ') !=-1:
                self.commandList.append(command)
                return True
        return False

    def _removeCommand(self,command):#command is dict with command and description
        if command in self.commandList:
            self.commandList.remove(command)
            return True
        else:
            return False

    async def on_ready(self):
        print('User: '+ self.client.user.name+' is activated.\nUsing Bot:'+title)
        isReady =True
        #load things here
        pass

    #call on messages here
    async def on_message(self,message):
        if message.content[0] ==".":#can listen?
            pass
        elif message.content[0] == self.key:#correct key
           found= message.content.find(" ",2)
           if found !=-1:#end of command
               await self.runCommand(message.content[1:found],
                                     message.content[found+1:].split(),
                                     message.channel)
           else:
               await self.runCommand(message.content[1:],
                                     [],
                                     message.channel)
           return True
        return False
            
    
    async def runCommand(self,command,instruction,channel):
        for com in self.commandList:
            if command ==com.name:
                print("Running "+com.name)
                output =com.run(instruction)
                print("Output: "+output)
                await self.client.send_message(channel, output)
                
                return True
        return False

    #user message, returns count# of messages
    #IGNORES messages with '.' as first character
    async def getMessages_User(self,userID="",count =150,oldskippedMessages=0):
        i = 0
        messageID =""
        messageList =[]

        async for message in self.client.logs_from(message.channel,count+oldskippedMessages):
            if count < i or oldskippedMessages ==0:#add uncounted messages
                messageID = message.author.id
                if message.content[0] != '.':
                    if userID == "":
                        messageList.append(message.content)
                    elif userID == messageID:
                        messageList.append(message.content)
                    else:
                        skippedMessages +=1
                else:
                    skippedMessages +=1

            i+=1
        if skippedMessages >0:#gets the exact count of messages because bot cannot see anything with '.'
            mmessageList.extend(getMessages_User(UserID,count+oldskippedMessages,skippedMessages))#dont read already skipped messages
        return messageList

    def getName(self,memberid,getNick):
        if getNick:
            return self.client.server[this.server].members.nick
        else:
            return self.client.server[this.server].members.name