#from bot import *#not required but helps with intelisense
#this will crash your command if you do use it

#parameters are taken as space seperated values after the command itself
#-commandExample thingOne 2
#     name       param1   peaches


#function can be anywhere in the file
#that isnt nested -aka dont put it inside a class

#function name must match command name
#function name must be 3 or more characters
#to use bot and command varibles add bot and command as parameters
#You can have as many or as few parameters as you want in any order

#all additional parameters are passed in as strings!!!

#add a id using the function name + "_id"       set it = to a uuid 
commandExample_id = '8a876646-bca2-4ae4-8a2f-809226ed7a16'
def commandExample(bot,command,param1: str,peaches: str):#keep this on one line
    goPrint ="Bot Name: "+bot.title+" command Name: "+command.name+"\n"
    goPrint ="Example :" +param1 +", "+peaches#Example :thingOne, 2


    #give your varibles unique names

    #bad example
    peachesLength =len(peaches)#the varible peachesLength will get confused as peaches

    #good example
    pLength = len(peaches)#does not have the word "peaches" in it

    if param1 >5:
        return "I like peaches"#returns can go anywhere in your function


    return goPrint#use return to print a string to the current channel


#multiple commands can be in a single file

#This command will not be read
commandExample_id = '8a876646-bca2-4ae4-8a2f-809226ed7a16'
def commandExample(bot,command,param1: str,peaches: str):
    return False


#NOT IMPLIMENTED YET

#new lines will be counted inside endless param
  #-paramExample true "These words are inside of double ticks" This is a story\n about how my life got turned upside down!
# single param->|    |                                        | the rest of these words are inside
#        normalParam        iamWords                            endlessParam
paramExample_id ='a72e3baf-03e9-4280-87c8-5009eb2a93ba'
def paramExample(bot, normalParam:str,iamWords:str, endlessParam ='to_end'):#set values equal to to_end if you want to read the rest of the input as 1 parameter
    #normalParam = true
    #endlass Param = "This is a story\n about how my life got turned upside down!"

    #example of converting strings to other value types
    normalBool =False
    if normalParam.lower in ['1','true','t','+','one']:
        normalBool =True


#ENTER seperated parameters
  #-paramsVertical 
  #true 
  #"These words are inside of double ticks" 
  #This is a story
  #about how my life got turned upside down!
paramsVertical_id ='a72e3baf-03e9-4280-87c8-5009eb2a93ba'
paramsVertical_options = 'vertical'#vertical option makes every line a new parameter
def paramsVertical(a, b, c, d):
    pass

#ENTER seperated parameters
#-paramsVertical 
twoPartExample_id ='a72e3baf-03e9-4280-87c8-5009eb2a93ba'

#any rank will work after wait
twoPartExample_options = 'wait'#wait waits for a response from the user
twoPartExample_options = 'wait-user'#wait waits for a response from the user
twoPartExample_options = 'wait-none'#default - doesnt wait
twoPartExample_options = 'wait-everyone'#wait waits for a response from the @everyone rank
twoPartExample_options = 'wait-mod'#wait waits for a response from @mod rank
twoPartExample_options = 'wait-bot'#wait waits for a response from a bot
def twoPartExample(a, b, c, d):
    pass