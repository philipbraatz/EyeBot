import uuid
import sys
from UtilityPrint import *

def safeRun(bot,command,params):
    if command.path != "":
        try:
            global ret
            ret = ""
            exec(command.function)
            return str(ret)
        except Exception as e:
            return ("Error in " + command.path + " " + command.name + ": " + str(e))
    else:
        return "Error: Command path does not exist"

class Parameter():
    value :str

    def __init__(self,command_Id:str,name:str,position:int,to_end:bool,required:bool):
        self.command_id :str = command_Id
        self.name :str = name
        self.position :int = position
        self.to_end :bool = to_end
        self.required:bool = required
        pass

    def __str__(self):
        return self.name#user see this message
        #return self.name + "[command_id:" + self.command_id + ",position:" + str(self.position) + ",to_end:" + str(self.to_end)#DEBUG
    pass

class Command(object):
    def __init__(self,bot,name,description = "",privliges = "ALL",path = "",vertical = False,wait = 'none',documentation:str = ""):
        self.id = str(uuid.uuid4())
        self.bot = bot#botself

        self.path = path
        self.name = name#called name
        self.description = description
        self.privlige = privliges#security level
        self.parameters :list = []
        self.minParamCount = 0
        self.documentation = documentation

        self.function = ""#actual command to run as text

        self.vertical = False
        self.wait = 'none'

        self.Error = "Loaded Succesfully"

        #stats
        self.stat_uses = 0
        self.stat_lastUse = ""#time
        self.stat_lastUser = ""#user id
        self.stat_created = ""#time
        self.stat_updated = ""#time

        try:
            if path == "" and len(self.name) > 2:
                self.path = "Commands\\python\\" + self.name + ".py"

                ##Future inprovement

                #self.path = "COmmands\\parsed\\"+self.name+".py"
                #if self.load == SUCCESS:
                #   self.function =self.load()

                #else:
                #   self.path = "Commands\\python\\"+self.name+".py"
                #
                #if self.load == SUCCESS:
                #   self.function =self.load()

                self.function = self.load()
                pass
            else:
                self.function = self.load()
                pass
            pass
        except Exception as e:
            log(self.name + " Had an error parsing",'u')
            self.Error = str(e)
            self.path = "Load Exception"
            
            pass

    def create(self,code):
        if path != "":
            file = open(self.path,"w")
            file.write(code)
            file.close()
            pass

    def findParameterOptions(self,parameter:str,position):
        name :str = ""
        to_end :bool = False
        required =True
        pfind :int = parameter.find(":") 
        if pfind != -1:
            name = parameter[:pfind]
            if parameter[pfind + 1:] != "str":
                raise SyntaxError("All parameters of a command must be passed as type \"str\"")
            
        pfind = parameter.find("=") 
        if pfind != -1:
            start = parameter.find("\"",pfind)
            if start == -1:
                start = parameter.find("\'",pfind)
                if start == -1:
                    raise SyntaxError("All parameters of a command must be passed as type \"str\"")
                end = parameter.find("\'",start + 1)
            else:
                end = parameter.find("\"",start + 1)
            #options =p[pfind:]
            name = parameter[:pfind]
            options :str = parameter[start + 1:end - 1]#find everything after parameters :
            if options == "to_end":
                to_end = True#custom to_end parameter
            else:
                self.minParamCount -=1#normal defaulting value
            pass
        else:
            #options = ""
            pass

        if name == "":
            name = parameter#simple 1 word parameter


        self.parameters.append(Parameter(self.id,name,position,to_end,required))#add to list
        pass


    #returns calling function + content
    def findAndReplaceFunction(self,content:str):
        paramsStart = content.find("(") + 1
        paramsEnd = content.find(")")
        log("Params Raw = " + content[paramsStart:paramsEnd],'d')

        paramList = content[paramsStart:paramsEnd].split(",")
        if paramList == [""]:
            paramList = []#remove empty parameter
        self.minParamCount = len(paramList)

        for i in range(len(paramList)):
            self.findParameterOptions(paramList[i],i)

        findName = content.find("def ") + len("def ")
        content = content[:paramsEnd + 2] + "\n    global ret\n    ret = \"\"" + content[paramsEnd + 2:]
        callFunction = content[findName:paramsStart]

        if len(self.parameters) == 0:#ZERO params
            log("no parameters",'d')
            return content + "\n" + callFunction + ")"#functionName()
        elif len(self.parameters) == 1:#ONE param
            log("ParamCount of 1",'d')
            log("Params Clean = " + str(paramList),'u')
            if self.parameters[0].name == "bot" or self.parameters[0].name == "command":#ONE normal param
                self.minParamCount = 0
            return content + "\n" + callFunction + self.parameters[0].name + ")"#functionName(param1)
        else:#more than ONE param
            place = 0
            for param in self.parameters:
                newParam =param.name#keep names and only temperaraly replace with params[i]
                if newParam != "bot" and newParam != "command":#rename extra parameters
                    #log("Param["+str(place)+"] = "+str(param))
                    content.replace(newParam,"params[" + str(place) + "]")
                    newParam = "params[" + str(place) + "]"
                    place +=1
                else:
                    self.minParamCount -=1
                    log("Removing Extras!",'t')
                log("next param "+param.name,'t')
                callFunction +=newParam + ","
            #callFunction +=param

            log("ParamCount = " + str(self.minParamCount),'d')
            log("Params Cleaned",'u')
            for p in self.parameters:
                print(p)
            return content + "\n" + callFunction + ")"
        

    def load(self):
        if self.path == "":
            return False

        log("\nLoading " + self.name,'u')

        callFunction = ""

        readfile = ""
        try:
            with open(self.path,"r") as f:
                for line in f:
                    readfile +=line
        except IOError:
            log("Could not read file: " + self.path,'u')
            
        #find start of function
        startDecleration = readfile.find("def " + self.name)#def functionName | Posistion
        if startDecleration > 0:
            readfile = readfile[startDecleration:]
        else:
            log("Skipping... could not find \"def " + self.name + "\"",'u')
            return False

        endFunction = readfile.find("def ",startDecleration + 1)
        if endFunction > 0:
            readfile = readfile[:endFunction]
        else:
            EndFunction = len(readfile)
        #log("Preprocessed:\n"+readfile,'t')#DEBUG

        #the end of the line after the function definition
        firstEndLine = readfile.find("\n",startDecleration,endFunction)#def functionName(bot,command, length) | Posistion
        if firstEndLine == -1:
            firstEndLine = endFunction

        if startDecleration > -1:#if there is a definition
            #log("setting varibles - Start: "+str(startDecleration)+" End:
                                             #"+str(endFunction),'t')#DEBUG varible
            readfile = self.findAndReplaceFunction(readfile)#convert to command Readable

        readfile = readfile.replace("return ","ret =")#replace returns with ret varible
        #readfile =(readfile).replace("\\","\\\\")#replace escape characters.
                                                              #do this last to
                                                                                                                    #get
                                                                                                                                                                          #everything
        log("\nFinal:\n" + readfile,'d')
        return readfile

    def run(self,params:list):
        #self.action =self.instruction
        global ret
        ret = "Error: Command did not execute"
        log("Type = " + str(type(params)),'t')
        if type(params) == type("this is a string"):
            params = [params]#make sure parameter doesnt get chopped up into type char
        if self.minParamCount <= len(params):
            result = safeRun(self.bot,self,params)
            log("Result command: " + result,'d')
            return result
        else:
            paramError = self.name + " takes a minimum of " + str(self.minParamCount) + " parameters\n"
            for p in self.parameters:
                paramError+=p.name + ", "
            return paramError

    def info(self,data:list,output = ""):
        if len(data) > 0:
            if "all" in data:
                output+= self.info(data ="names parameters doc stats".split(),output=output)
            else:
                if "doc" in data:
                    output+="\n\n" + self.documentation + "\n\n"
                if "names" in data:
                    output+="Bot ID: " + self.bot.id + "\n"
                    output+="Bot Name: " + self.bot.title + "\n"
                    output+="ID: " + self.id + "\n"
                    output+="Name: " + self.name + "\n"
                if "stats" in data:
                    output+="Uses: " + str(self.stat_uses) + "\n"
                    output+="Created on: " + str(self.stat_created) + "\n"
                    output+="Last updated: " + str(self.stat_updated) + "\n"
                if "advanced" in data:
                    output+="last use: " + str(self.stat_lastUse) + "\n"
                    output+="Last User: " + str(self.stat_lastUser) + "\n"
                    output+="File: " + self.path + "\n"
                if "parameters" in data:
                    output+="Minimum Parameters: " + str(self.minParamCount) + "\nParameters:\n"
                    for p in self.parameters:
                            output+=str(p) + ", "
                    output+="\n"
                    if self.vertical:
                        output+="Read type: Vertical " + self.wait + "\n"
                    else:
                        output+="Read type: Horizontal " + self.wait + "\n"
                if "function" in data:
                    output+= self.function
        else:
            return "please add options: doc, names, stats, advanced, parameters, function, or all"
        return output
pass

class CommandList(list):
    def __init__(self,comList:list):
        self.extend(comList)
        pass
                
    def is_command(self,name:str):
        if len(name) < 3:
            #print(name+" is not command")
            return False

        for c in self:
            if c.name == name:
                return True
        else:
            #print(name+" is not command")
            return False

    def run_command(self,name:str, parameters:str):
        for c in self:
            if c.name == name:
                if c.vertical:
                    return c.run(parameters.split('\n'))
                else:
                    return c.run(parameters.split(' '))
        else:
            return "command " + name + " does not exist"

    def get_info(self,name:str,data:list):
        print("Checking " + str(data))
        for c in self:
            if c.name == name:
                return c.info(data)
        else:
            return "command " + name + " does not exist"

