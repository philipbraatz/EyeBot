#from bot import *

help_id = '25bafbb1-49fc-4ad8-9419-3de211148c6a'
def help(bot):
    ret = bot.title+":\n"+bot.desc
    ret+="\nKey \""+bot.key+"\" "
    ret+="\nName\t\tDescription\n"
    for com in bot.commandList:
        if len(com.name) >2:
            ret+=bot.key+com.name+"\t\t|"+com.description+"\t\t\n"
        else:
            ret+=com.name+"\t\t|"+com.description+"\t\t\n"
    return ret

add_id = '4ddb6548-6d19-4389-9546-d1213db7d28b'
def add(a,b):
    return int(a)+int(b)

ping_id = '690316a0-16d1-4ae8-a31b-12c07554b067'
def ping():
    return "Pong"

command_id = 'a5fdc34e-d414-44e5-b9ee-518303ee901e'
def command(bot, mode,name,description="",privledge ="",vertical=True,wait='none',filepath='',function='to_end'):
    if mode == "add":
        pass
    elif mode == "update":
        pass
    elif mode == "delete":
        pass
    elif mode == "reload":

        pass
    else:
        pass
    pass