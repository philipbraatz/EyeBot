def safeRun(bot,command,params):
    if command.path != "":
        exec(command.function)
        return ret
    else:
        return "Error: Command path does not exist"

class command(object):


    def __init__(self,bot,name,description="",privliges="ALL",path=""):
        self.name=name#called name
        self.description=description
        self.privlige=privliges#security level

        if path != "":
            self.bot = bot#botself
            self.path =path#file or something crazyss
            self.function =self.load()
            pass

    def create(self,code):
        if path != "":
            file = open(self.path,"w")
            file.write(code)
            file.close()
            pass

    #returns calling function + content
    def findAndReplaceParameters(self,content:str):
        paramsStart = content.find("(")
        paramsEnd = content.find(")")
        paramStart =paramsStart

        findName=content.find("def ")+len("def ")
        #print("Find Content---\n"+content+"\n\n")
        print("Namestart: "+str(findName)+" NameEnd"+str(paramsStart))
        functionName = content[findName:paramsStart]
        content =content[:paramsEnd+2]+"\n    global ret\n"+content[paramsEnd+2:]
        print("functionName ="+functionName)
        callFunction = functionName+"("

        paramEnd =content.find(",",paramsStart,paramsEnd)-1#place before comma
        if paramEnd <= -1:#only has 1 parameter
            paramEnd = paramsEnd#end of parameters
        param = content[paramsStart:paramEnd].strip()#(parameter1, param2)
        if len(param) == 0:#()
            return content+"\n"+callFunction+")"#functionName()

        self.paramCount  =0
        while paramEnd <=-1:
            print(str(paramCount) + " paramEnds ="+str(paramEnd)+" | " + param)
            #print("replacing \""+param+"\"")
            if param != "bot" and param !="command":#rename extra parameters
                content.replace(param,"params["+str(paramCount)+"]")
                param ="params["+str(paramCount)+"]"
                self.paramCount +=1
                pass

            callFunction +=param

            paramStart+=len(param)+1#go to next param after comma
            paramEnd =content.find(",",paramsStart,paramsEnd)-1
            if paramEnd == -1 or paramEnd > paramsEnd:#last varible
                return content+"\n"+callFunction+")"
            else:
                callFunction+= ","
            param =content[paramStart:paramEnd].strip()
        return content+"\n"+callFunction+")"
        
    def load(self):
        print("\nLoading "+self.name)
        if self.path != "":
            callFunction=""

            readfile =""
            with open(self.path,"r") as f:
                for line in f:
                    readfile +=line
            
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
                readfile = self.findAndReplaceParameters(readfile)

            readfile =readfile.replace("return ","ret =")#replace returns with ret varible
            readfile =(readfile).replace("\\","\\\\")#replace escape characters. do this last to get everything
            print("Final:\n"+readfile)
            return readfile

    def run(self,params):
        #self.action =self.instruction
        global ret
        ret =None
        if self.paramCount == len(params):
            return safeRun(self.bot,self,params)
        else:
            return self.name+ " takes "+str(self.paramCount)+" parameters"
pass