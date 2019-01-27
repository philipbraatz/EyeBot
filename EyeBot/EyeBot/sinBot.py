from bot import Bot
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
    ID =""
    name ="Unnamed Sin"
    healthBase =-1
    attackBase =-1
    stype =""

    WordList = []#List of sentences with List of words nested

    curHealth=health
    dead =False

    dmgTaken =0
    dmgDelt=0

    def __init__(self,time,name, attacklines,sinID):
        time = time % 100000000
        sinID =int(sinID[0:8])
        self.ID =str(abs(time-sinID))#string of random numbers

        self.name =name
        __getlines__(self,attacklines)

        pass

    def __getlines__(self,attackMessages):
        self.WordList =[]#clear list
        for line in attackMessages:
            self.WordList.append( line.split())
            pass
        pass

    def setHealthBase(self,health):
        self.healthBase =health
        self.curHealth =health
        pass

    def getHealth(self,health):
        return self.curHealth
    def takeDamage(self,damage,type):
        self.curHealth -=typeAdvantage[self.stype][type] * damage
        if curHealth <1:
            self.dead = True
            self.curHealth =0
        pass

class sinGod(object):
    level =0
    ID =""#player ID
    minons =[]#list of sinners

    wildWins=0#won wild battles
    wildLoss=0
    godWins=0#won battles
    godLoss=0

    def __init__(self,ID):
        self.ID =ID
        pass

    def add_minon(self,sinner):
        self.minons.append(sinner)
        pass

    def remove_minon(self,sinner):
        self.minons.remove(sinner)
        pass


class sinGame(Bot):
    ID={
        "wild":"",
        "arena":""
        }

    filePlayers="sinimonPlayers.txt"
    sinPlayers =[]#list of sinGods
    serverMembers=[]#list of members

    def __init__(self,server, client, Comkey, title, desc, wild ="",arena=""):
        self.ID["wild"] =wild
        self.ID["arena"]=arena

        #Debug Admin commands
        self.addCommand({"Command":"!addme","Desc":"test adding a player","Priv":"ADMIN"})

        return super().__init__(client, server, "", Comkey, title, desc)

    def loadPlayers(self):
        with open(self.filePlayers,"r") as file:
            self.filePlayers=json.load(file)
    def savePlayers(self):
        with open(self.filePlayers,"w") as file:
            json.dump(self.sinPlayers,file)

    #adds only new players
    #returns location in list
    def addNewPlayer(self,playerID):
        if self.sinPlayers >0:
            pcount =-1
            for player in self.sinPlayers:
                pcount+=1
                if player.ID == playerID:
                    return pcount
        self.sinPlayers.append(sinGod(playerID))
        return len(self.sinPlayers)-1

    #deletes player
    #returns deleted location
    def deletePlayer(self,playerID):
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

    def generateSin(self,sinID,time):
        retSin =sinner(time,sinID,super(Bot,self).getMessages_User(sinID),sinID)
        return retSin