import discord
from discord.ext import commands
from typing import List
from Command import *

global isReady
isReady = False

class Bot():

    ready = False

    client = ""
    
    key = ""

    server = ""
    channelList: list = []#{"ID":"","Type":""}

    commandList:list = []
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

    def _checkcommand(self,command):#command is dict with command and description
        pass

    def _addCommand(self,command):#command is dict with command and description and privledge
        pass

    def _removeCommand(self,command):#command is dict with command and description
        if command in self.commandList:
            self.commandList.remove(command)
            return True
        else:
            return False

    async def on_ready(self):
        print('User: '+ self.client.user.name+' is activated.\nUsing Bot:'+self.title)
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
        pass

    def getName(self,memberid,getNick):
        if getNick:
            return self.client.server[this.server].members.nick
        else:
            return self.client.server[this.server].members.name