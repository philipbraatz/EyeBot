def help(bot):
    print("inside help")
    ret = self.bot.title+":\n"+self.bot.desc
    for com in self.bot.commandList:
        ret+="\nName\t\tDescription\t\t\n"
        ret+=com.name+"\t\t"+com.description+"\t\t\n"
    return ret

def add(a,b):
    return a+b

def ping():
    return "Pong"