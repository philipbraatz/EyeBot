import discord
from discord.ext import commands

global isReady
isReady =False

class member(object):
    def __init__(self, id,command, help):
        self.id = id
        self.name =client.get_server(id)

class Bot(object):

    ready =False

    client =""
    
    key =""

    server = ""
    channel =""

    commandList =[]
    curMessage={"Command":"","Desc":"","Priv":""}
    curCommand =""
    curInstruction=""

    previousMessage=""

    title =""
    desc =""
    def __init__(self,client, serverID, channelID, key,title,desc):
        self.client =client
        self.server =serverID
        self.channel =channelID
        self.key = key

        help =[{"command":"help","desc":"shows this list"},
                {"command":".","desc":"Bot cannot see messages that start with ."}]
        self.commandList =[help]

        self.title =title
        self.desc =desc

    def getCommands(self):
        return commandList

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

    def parse(self, text):
        if text[0] =='.':
            pass
        elif text[0] == key:
           found= text.find(' ',2)
           if found !=-1:
               self.curCommand =text[1:found]
               self.curInstruction =text[found+1:]
               return True
        return False

    def help_command(self):#returns info and commands
        ret = self.title+":\n"+self.desc
        for com in commandList:
            ret+="\n"
            for key,value in commandList[c]:
                if key == "command":
                    ret+=com[key]+"\t-"
                if key =="desc":
                    ret+=com[key]+"."
        return ret

    async def on_ready(self):
        print('User: '+ self.client.user.name+' is activated.\nUsing Bot:'+title)
        isReady =True
        #load things here
    async def on_message(self,message):
        parse(message)
        self.runCommands()
        pass

    def runCommands(self,command,userID):
        pass

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

    def getName(self, serverID,memberid,getNick =true):
        if getNick:
            return self.client.server[serverID].members.nick
        else:
            return self.client.server[serverID].members.name