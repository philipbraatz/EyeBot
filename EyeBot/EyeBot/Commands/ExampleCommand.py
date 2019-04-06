#parameters are taken as space seperated values after the command itself
#-commandExample thingOne 2
#     name       param1   param2


#function can be anywhere in the file
#that isnt nested - dont put it inside a class

#function name must match command name
#to use bot and command varibles add bot and command as parameters
#You can have as many or as few parameters as you want
#all additional parameters are passed in as strings
def commandExample(bot,command,param1: str,peaches: str):
    goPrint ="Bot Name: "+bot.title+" command Name: "+command.name+"\n"
    goPrint ="Example :" +param1 +", "+peaches#Example :thingOne, 2


    #give your varibles unique names

    #bad example
    peachesLength =len(peaches)#the varible peachesLength will get confused as peaches

    #good example
    pLength = len(peaches)#does not have the word "peaches" in it

    #this can go anywhere in your function
    return goPrint#use return to print a string to the current channel