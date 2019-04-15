import uuid

def safeRun(bot,command,params):
    if command.path != "":
        try:
            exec(command.function)
            return str(ret)
        except:
            return ("Error in "+command.name+" "+command.path+": "+ sys.exc_info()[0])

    else:
        return "Error: Command path does not exist"

class command(object):


    def __init__(self,bot,name,description="",privliges="ALL",path = ""):
        self.id = str(uuid.uuid4())
        self.name=name#called name
        self.description=description
        self.privlige=privliges#security level
        self.bot = bot#botself
        self.paramCount =0
        self.path = path
        self.function=""

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
        paramList = content[paramsStart:paramsEnd].split(",")
        self.paramCount =len(paramList)

        findName=content.find("def ")+len("def ")
        content =content[:paramsEnd+2]+"\n    global ret\n    ret = \"\""+content[paramsEnd+2:]
        callFunction = content[findName:paramsStart]

        print("ParamCount = "+str(self.paramCount))
        if len(paramList) == 0:
            return content+"\n"+callFunction+")"#functionName()
        elif len(paramList) ==1:
            return content+"\n"+callFunction+paramList[0]+")"#functionName(param1)
        else:
            p =0
            for param in paramList:
                print("replacing \""+param+"\"")
                if param != "bot" and param !="command":#rename extra parameters
                    print("Param["+str(p)+"] = "+str(param))
                    content.replace(param,"params["+str(p)+"]")
                    param ="params["+str(p)+"]"
                p +=1

                callFunction +=param+","
            #callFunction +=param
            return content+"\n"+callFunction+")"
        
    def load(self):
        print("\nLoading "+self.name)
        if self.path != "":
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

            endFunction =readfile.find("def ",startDecleration+1)
            if endFunction >0:
                readfile =readfile[:endFunction]
            else:
                EndFunction = len(readfile)
            print("Preprocessed:\n"+readfile)

            #the end of the line after the function definition
            firstEndLine =readfile.find("\n",startDecleration,endFunction)#def functionName(bot,command, length) | Posistion
            if firstEndLine == -1:
                firstEndLine = endFunction

            if startDecleration >-1:#if there is a definition
                print("setting varibles - Start: "+str(startDecleration)+" End: "+str(endFunction))
                readfile = self.findAndReplaceParameters(readfile)#convert to command Readable

            readfile =readfile.replace("return ","ret =")#replace returns with ret varible
            #readfile =(readfile).replace("\\","\\\\")#replace escape characters. do this last to get everything
            print("\nFinal:\n"+readfile)
            return readfile

    def run(self,params):
        #self.action =self.instruction
        global ret
        ret = "Error: Command did not execute"
        if self.paramCount == len(params):
            return safeRun(self.bot,self,params)
        else:
            return self.name+ " takes "+str(self.paramCount)+" parameters"
pass