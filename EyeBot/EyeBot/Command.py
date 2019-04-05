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
            self.path =path#file or something crazy
            self.function =self.load()
            pass

    def create(self,code):
        if path != "":
            file = open(self.path,"w")
            file.write(code)
            file.close()
            pass

    def load(self):
        if self.path != "":
            callFunction=""

            readfile =""
            with open(self.path,"r") as f:
                for line in f:
                    readfile +=line

            #find start of function
            print("Original:\n"+readfile+"\n\n")
            endDecleration =readfile.find("def "+self.name)#def functionName | Posistion

            #the end of the line after the function definition
            firstEndLine =readfile.find("\n",endDecleration)#def functionName(bot,command, length) | Posistion
            if endDecleration >-1:#if there is atleast 2 lines of data

                parameters =-1
                callFunction =self.name+"(bot,command"#functionName(bot,command,
                print("46:"+callFunction)
                paramLoc =readfile.find(",",endDecleration,firstEndLine)#current parameters location

                if paramLoc !=-1:#more than 1 parameter
                    callFunction+=","
                    print("51:"+callFunction)
                    param = readfile[readfile.find("(",endDecleration,firstEndLine):paramLoc].strip()#first param

                    #Replace all parameters with proper varibles
                    while(paramLoc>-1):

                        #convert parameters to usable values
                        if(param != "bot" and param !="command"):
                            parameters+=1
                            lastFound =readfile.find(param,firstEndLine)
                            while(lastFound >-1):
                                readfile =readfile.replace(param,"params["+str(parameters)+"]")
                                pass
                            pass

                        #Load next parameter
                        paramLoc =readfile.find(",",paramLoc,firstEndLine)#start of param
                        paramEnd =readfile.find(",",paramLoc,firstEndLine)#end of param
                        if paramEnd == -1:
                            paramEnd =readfile.find(")",paramLoc,firstEndLine)#last param
                        param =readfile[paramLoc+1:paramEnd].strip()
                        print(param)
                        callFunction +=param+","#functionName(bot,command,params[0],params[1]
                        print("73:"+callFunction)
                        pass
                else:#0 or 1 parameter
                    param = readfile[readfile.find("(",endDecleration,firstEndLine)+1:
                                     readfile.find(")",endDecleration,firstEndLine)]#only param inside ()
                    if(param != "bot" and param !="command"):
                        if len(param.strip()) >0:
                            readfile =readfile.replace(param.strip(),"params[0]")
                        print(param)

                callFunction+=")"#functionName(bot,command,params[0],params[1])
                print("85:"+callFunction)
                if parameters <0:
                    parameters =0
                self.paramCount =parameters
                readfile =readfile.replace("return ","ret =")#replace returns with ret varible
                pass

            
            
            
            readfile =(("global ret\n"+ #add Global varibles
                       callFunction +"\n"+#call function
                       readfile)        #before file ^
                        .replace("\\","\\\\"))#replace escape characters
            print(readfile)
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