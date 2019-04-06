from bot import Bot
from typing import List
import json

#attacker->victim
typeAdvantage = {
    "Envy":{
        "Envy":1,
        "Greed":2,
        "Lust":1,
        "Gluttony":1,
        "Wrath":1,
        "Sloth":1,
        "Pride":1
    },
    "Greed":{
        "Envy":1,
        "Greed":1,
        "Lust":1,
        "Gluttony":2,
        "Wrath":1,
        "Sloth":1,
        "Pride":1
    },
    "Lust":{
        "Envy":1,
        "Greed":1,
        "Lust":1,
        "Gluttony":1,
        "Wrath":1,
        "Sloth":2,
        "Pride":1
    },
    "Gluttony":{
        "Envy":2,
        "Greed":1,
        "Lust":1,
        "Gluttony":1,
        "Wrath":1,
        "Sloth":1,
        "Pride":1
    },
    "Wrath":{
        "Envy":1,
        "Greed":1,
        "Lust":1,
        "Gluttony":1,
        "Wrath":1,
        "Sloth":1,
        "Pride":2
    },
    "Sloth":{
        "Envy":1,
        "Greed":1,
        "Lust":2,
        "Gluttony":1,
        "Wrath":1,
        "Sloth":1,
        "Pride":1
    },
    "Pride":{
        "Envy":1,
        "Greed":1,
        "Lust":1,
        "Gluttony":1,
        "Wrath":2,
        "Sloth":1,
        "Pride":1
    }
}

#created by the ID, time, and sinGod 
class sinner(object):
    ID: str =""
    name: str ="Unnamed Sin"
    healthBase: int =-1
    attackBase:int =-1
    stype:str =""

    WordList: List[str] = []#List of sentences with List of words nested

    dead: bool =False

    dmgTaken:int =0
    dmgDelt:int=0

    def __init__(self,time:int,name:str, attacklines:List[str],sinID:str):
        time = time % 100000000
        sinID =sinID[0:8]
        self.ID =str(abs(time-int(sinID)))#string of random numbers

        self.name =name
        #__getlines__(self,attacklines)

        self.curHealth: int=self.healthBase

        pass

    def __getlines__(self,attackMessages:List[str]):
        self.WordList =[]#clear list
        for line in attackMessages:
            self.WordList.extend( line.split())
            pass
        pass

    def setHealthBase(self,health:int):
        self.healthBase =health
        self.curHealth =health
        pass

    def getHealth(self,health:int):
        return self.curHealth
    def takeDamage(self,damage:int,type:str):
        self.curHealth -=typeAdvantage[self.stype][type] * damage
        if self.curHealth <1:
            self.dead = True
            self.curHealth =0
        pass

class sinGod(object):
    level:int =0
    ID:str =""#player ID
    minons:List[sinner] =[]#list of sinners

    wildWins=0#won wild battles
    wildLoss=0
    godWins=0#won battles
    godLoss=0

    def __init__(self,ID:str):
        self.ID =ID
        pass

    def add_minon(self,sinner:sinner):
        self.minons.append(sinner)
        pass

    def remove_minon(self,sinner:sinner):
        self.minons.remove(sinner)
        pass


class sinGame(Bot):
    ID={
        "wild":"",
        "arena":""
        }

    filePlayers="sinimonPlayers.txt"
    sinPlayers: List[sinGod] =[]#list of sinGods
    serverMembers:List[str]=[]#list of members

    def __init__(self,server:str, client:str, Comkey:str, title:str, desc:str, wild:str ="",arena:str=""):
        self.ID["wild"] =wild
        self.ID["arena"]=arena

        #Debug Admin commands
        self._addCommand({"Command":"!addme","Desc":"test adding a player","Priv":"ADMIN"})

        return super().__init__(client, server, "", Comkey, title, desc)

    def loadPlayers(self):
        with open(self.filePlayers,"r") as file:
            self.filePlayers=json.load(file)
    def savePlayers(self):
        with open(self.filePlayers,"w") as file:
            json.dump(self.sinPlayers,file)

    #adds only new players
    #returns location in list
    def addNewPlayer(self,playerID:str):
        if len(self.sinPlayers) >0:
            pcount =-1
            for player in self.sinPlayers:
                pcount+=1
                if player.ID == playerID:
                    return pcount
        self.sinPlayers.append(sinGod(playerID))
        return len(self.sinPlayers)-1

    #deletes player
    #returns deleted location
    def deletePlayer(self,playerID:str):
        pcount =-1
        for player in self.sinPlayers:
            pcount+=1
            if player.ID == playerID:
                del self.sinPlayers[pcount]
                return pcount
        return -1

    def loadMembers(self):
        lserver =client.get_server(server)
        for member in lserver.members:
            self.serverMembers.append(member.id)
        pass

    def generateSin(self,sinID:str,time:int):
        retSin =sinner(time,sinID,super(Bot,self).getMessages_User(sinID),sinID)
        return retSin