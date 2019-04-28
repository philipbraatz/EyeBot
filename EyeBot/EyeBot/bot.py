import discord
from discord.ext import commands
from typing import List
from Command import *
import uuid

global IsReady
IsReady = False

class Bot():

    
    def getCommands(self):
        return self.commands

    #curMessage={"Command":"","Desc":"","Priv":""}


    #previousMessage=""

    def __init__(self,client, serverID:str, channelSet:str, key:str,title:str,desc:str):

        self.ready :bool = False

        self.id = str(uuid.uuid4())#TODO impliment saving of bots
        self.client = client
        self.server = serverID
        #self.channelList: list =channelSet
        self.key = key
        
        defaultFile ="Commands\\python\\Default.py"
        self.commands = CommandList([Command(self,"help","shows this list","ALL",defaultFile),
            Command(self,".","Bot cannot see messages that start with .","ALL"),
            Command(self,self.key + self.key,"Get command information","NERD MOD"),
            Command(self,"ping","Check if bot is responding","ALL",defaultFile),
            Command(self,"error","prints command error","NERD",defaultFile),
            #command(self,"add","adds 2
            #numbers","ALL","Commands\\python\\Default.py"),
            Command(self,"command","Modify commands","MOD",defaultFile),])

        self.title :str = title
        self.desc :str = desc
        pass

    async def on_ready(self):
        print('User: ' + self.client.user.name + ' is activated.\nUsing Bot:' + self.title)
        isReady = True
        #load things here
        pass

    #call on messages here
    async def on_message(self,message):
        if message.content[0] == ".":#can listen?
            pass
        elif message.content[0:2] == self.key + self.key:#Override
            print("Description")
            found = message.content.find(" ",2)
            if found == -1:#end of command
                found = len(message.content)
            print(str(found))
            if self.commands.is_command(message.content[2:found]):
                print("is command == true")
                await message.channel.send(self.commands.get_info(message.content[2:found],
                    message.content[found + 1:].split()))
            pass
        elif message.content[0] == self.key:#correct key
           found = message.content.find(" ",2)
           if found != -1:#end of command
                await self.runCommand(message.content[1:found],
                        message.content[found + 1:],
                        message.channel)
           else:
               await self.runCommand(message.content[1:],
                                     [],
                                     message.channel)
           return True
        return False

    async def runCommand(self,command,instruction,channel):
        for com in self.commands:
            if command == com.name:
                #print("Running "+self.key + com.name +" with instructions: "+str(instruction))
                output = com.run(instruction)
                if len(output) >0:
                    print("Output: " + output)
                    await channel.send(output)
                else:
                    print("Command Finished")
                
                return True
        return False

    #user message, returns count# of messages
    #IGNORES messages with '.' as first character
    async def getMessages_User(self,userID="",count=150,oldskippedMessages=0):
        NotImplementedError
        pass

    def getName(self,memberid,getNick):
        if getNick:
            return self.client.server[self.server].members.nick
        else:
            return self.client.server[self.server].members.name