import uuid
import sys

def safeRun(bot,command,params):
    if command.path != "":
        try:
            exec(command.function)
            return str(ret)
        except Exception as e:
            return ("Error in "+command.path+" "+command.name+": "+ str(e))

    else:
        return "Error: Command path does not exist"

class command(object):


    def __init__(self,bot,name,description="",privliges="ALL",path = "",vertical =False,wait='none',documentation:str=""):
        self.id = str(uuid.uuid4())
        self.bot = bot#botself

        self.path = path
        self.name=name#called name
        self.description=description
        self.privlige=privliges#security level
        self.parameters:list =[]
        self.minParamCount =0
        self.documentation =documentation

        self.function=""#actual command to run as text

        self.vertical =False
        self.wait = 'none'

        #stats
        self.stat_uses =0
        self.stat_lastUse =""#time
        self.stat_lastUser =""#user id
        self.stat_created =""#time
        self.stat_updated =""#time

        if path == "" and len(self.name)>2:
            self.path = "Commands\\python\\"+self.name+".py"

            ##Future inprovement

            #self.path = "COmmands\\parsed\\"+self.name+".py"
            #if self.load == SUCCESS:
            #   self.function =self.load()

            #else:
            #   self.path = "Commands\\python\\"+self.name+".py"
            #
            #if self.load == SUCCESS:
            #   self.function =self.load()

            self.function =self.load()
            pass
        else:
            self.function =self.load()
            pass
        pass

    def create(self,code):
        if path != "":
            file = open(self.path,"w")
            file.write(code)
            file.close()
            pass

    #returns calling function + content
    def findAndReplaceParameters(self,content:str):
        paramsStart = content.find("(")+1
        paramsEnd = content.find(")")
        print("Params Raw = "+content[paramsStart:paramsEnd])
        self.parameters = content[paramsStart:paramsEnd].split(",")
        if self.parameters == [""]:
            self.parameters =[]#remove empty parameter
        self.minParamCount =len(self.parameters)

        #get rid of parameter formatting
        for i in range(len(self.parameters)):
            pfind =self.parameters[i].find(":") 
            #print("Found : in "+self.parameters[i])
            if pfind > -1:
                #options =p[pfind:]
                if self.parameters[i] != "bot" and self.parameters[i] !="command":
                    self.minParamCount -=1
                self.parameters[i] =self.parameters[i][:pfind]
            else:
                pfind =self.parameters[i].find("=")
                if pfind > -1:
                    if self.parameters[i] != "bot" and self.parameters[i] !="command":
                        self.minParamCount -=1
                    #options =p[pfind:]
                    self.parameters[i] =self.parameters[i][:pfind]
            #print("Pretty: "+self.parameters[i])

        findName=content.find("def ")+len("def ")
        content =content[:paramsEnd+2]+"\n    global ret\n    ret = \"\""+content[paramsEnd+2:]
        callFunction = content[findName:paramsStart]

        if len(self.parameters) == 0:#ZERO params
            print("no parameters")
            return content+"\n"+callFunction+")"#functionName()
        elif len(self.parameters) ==1:#ONE param
            print("ParamCount of 1")
            print("Param Clean = "+str(self.parameters))
            if self.parameters[0] == "bot" or self.parameters[0] =="command":#ONE normal param
                self.minParamCount =0
            return content+"\n"+callFunction+self.parameters[0]+")"#functionName(param1)
        else:#more than ONE param
            place =0
            for param in self.parameters:
                if param != "bot" and param !="command":#rename extra parameters
                    #print("Param["+str(place)+"] = "+str(param))
                    content.replace(param,"params["+str(place)+"]")
                    param ="params["+str(place)+"]"
                    place +=1
                else:
                    self.minParamCount -=1
                    print("Removing Extras!")
                callFunction +=param+","
            #callFunction +=param

            print("ParamCount = "+str(self.minParamCount))
            print("Params Clean = "+str(self.parameters))
            return content+"\n"+callFunction+")"
        
    def load(self):
        if self.path == "":
            return False

        print("\nLoading "+self.name)

        callFunction=""

        readfile =""
        try:
            with open(self.path,"r") as f:
                for line in f:
                    readfile +=line
        except IOError:
            print("Could not read file: "+self.path)
            
        #find start of function
        startDecleration =readfile.find("def "+self.name)#def functionName | Posistion
        if startDecleration >0:
            readfile =readfile[startDecleration:]
        else:
            print("Skipping... could not find \"def "+self.name+"\"")
            return False

        endFunction =readfile.find("def ",startDecleration+1)
        if endFunction >0:
            readfile =readfile[:endFunction]
        else:
            EndFunction = len(readfile)
        #print("Preprocessed:\n"+readfile)#DEBUG

        #the end of the line after the function definition
        firstEndLine =readfile.find("\n",startDecleration,endFunction)#def functionName(bot,command, length) | Posistion
        if firstEndLine == -1:
            firstEndLine = endFunction

        if startDecleration >-1:#if there is a definition
            #print("setting varibles - Start: "+str(startDecleration)+" End: "+str(endFunction))#DEBUG varible
            readfile = self.findAndReplaceParameters(readfile)#convert to command Readable

        readfile =readfile.replace("return ","ret =")#replace returns with ret varible
        #readfile =(readfile).replace("\\","\\\\")#replace escape characters. do this last to get everything
        print("\nFinal:\n"+readfile)
        return readfile

    def run(self,params):
        #self.action =self.instruction
        global ret
        ret = "Error: Command did not execute"
        if self.minParamCount <= len(params):
            return safeRun(self.bot,self,params)
        else:
            paramError =self.name+ " takes a minimum of "+str(self.minParamCount)+" parameters\n"
            for p in self.parameters:
                paramError+=p+", "
            return paramError

    def info(self,data:list,output=""):
        if len(data)>0:
            if "all" in data:
                output+= self.info(data ="names parameters doc stats".split(),output=output)
            else:
                if "doc" in data:
                    output+="\n\n"+self.documentation+"\n\n"
                if "names" in data:
                    output+="Bot ID: "+self.bot.id+"\n"
                    output+="Bot Name: "+self.bot.title+"\n"
                    output+="ID: "+self.id+"\n"
                    output+="Name: "+self.name+"\n"
                if "stats" in data:
                    output+="Uses: "+str(self.stat_uses)+"\n"
                    output+="Created on: "+str(self.stat_created)+"\n"
                    output+="Last updated: "+str(self.stat_updated)+"\n"
                if "advanced" in data:
                    output+="last use: "+str(self.stat_lastUse)+"\n"
                    output+="Last User: "+str(self.stat_lastUser)+"\n"
                    output+="File: "+self.path+"\n"
                if "parameters" in data:
                    output+="Minimum Parameters: "+str(self.minParamCount)+"\nAll  Parameters"
                    for p in self.parameters:
                            output+=p+", "
                    if self.vertical:
                        output+="Read type: Vertical "+self.wait
                    else:
                        output+="Read type: Horizontal "+self.wait
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
            return "command "+name+" does not exist"

    def get_info(self,name:str,data:list):
        print("Checking "+str(data))
        for c in self:
            if c.name == name:
                return c.info(data)
        else:
            return "command "+name+" does not exist"

