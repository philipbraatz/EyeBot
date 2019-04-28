class test():
    def findParameterOptions(self,parameter,position):
            name :str =""
            to_end :bool = False
            pfind :int = parameter.find(":") 
            if pfind != -1:
                name = parameter[:pfind]
                if parameter[pfind+1:] != "str":
                    raise SyntaxError("All parameters of a command must be passed as type \"str\"")
            
            pfind = parameter.find("=") 
            if pfind != -1:
                start = parameter.find("\"",pfind)
                if start == -1:
                    start = parameter.find("\'",pfind)
                    if start == -1:
                        raise SyntaxError("All parameters of a command must be passed as type \"str\"")
                    end =parameter.find("\'",start+1)
                else:
                    end =parameter.find("\"",start+1)
                #options =p[pfind:]
                name = paramList[i][:pfind]
                options :str = parameter[start+1:end-1]#find everything after parameters :
                if options == "to_end":
                    to_end = True#custom to_end parameter
                else:
                    self.minParamCount -=1#normal defaulting value
                pass
            else:
                #options = ""
                pass

            if name == "":
                name =parameter#simple 1 word parameter


            self.parameters.append(Parameter(self.id,name,position,to_end))#add to list
            pass


    #returns calling function + content
    def findAndReplaceFunction(self,content:str):
        paramsStart = content.find("(") + 1
        paramsEnd = content.find(")")
        print("Params Raw = " + content[paramsStart:paramsEnd])

        paramList = content[paramsStart:paramsEnd].split(",")
        if paramList == [""]:
            paramList = []#remove empty parameter
        self.minParamCount = len(paramList)

        for i in range(len(paramList)):
            findParameterOptions(paramList,i)

        findName = content.find("def ") + len("def ")
        content = content[:paramsEnd + 2] + "\n    global ret\n    ret = \"\"" + content[paramsEnd + 2:]
        callFunction = content[findName:paramsStart]

        if len(self.parameters) == 0:#ZERO params
            print("no parameters")
            return content + "\n" + callFunction + ")"#functionName()
        elif len(self.parameters) == 1:#ONE param
            print("ParamCount of 1")
            print("Params Clean = " + str(paramList))
            if self.parameters[0].name == "bot" or self.parameters[0].name == "command":#ONE normal param
                self.minParamCount = 0
            return content + "\n" + callFunction + self.parameters[0].name + ")"#functionName(param1)
        else:#more than ONE param
            place = 0
            for param in self.parameters:
                if param.name != "bot" and param.name != "command":#rename extra parameters
                    #print("Param["+str(place)+"] = "+str(param))
                    content.replace(param.name,"params[" + str(place) + "]")
                    param.name = "params[" + str(place) + "]"
                    place +=1
                else:
                    self.minParamCount -=1
                    print("Removing Extras!")
                callFunction +=param.name + ","
            #callFunction +=param

            print("ParamCount = " + str(self.minParamCount))
            print("Params Cleaned")
            for p in self.parameters:
                print(p)
            return content + "\n" + callFunction + ")"
        pass
    pass
pass

t =test()
t.findAndReplaceFunction("def foo(bot, param1, ploof:str,pop=\"to_end\")")