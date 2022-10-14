import sys

def serverFromCmd():
    if len(sys.argv) > 1 :
        url= sys.argv[1]
        if ':' in url :
            url= url.split(":")
            host= url[0]
            port= int(url[1])
        else :
            host= url
            port= 1400
    else :
        host= 'localhost'
        port= 1400
    return host, port

class StartCmd() :
    def __init__( self, gameName, modeLst, options= {}, parameters= {} ) :
        self.cmd= "."
        self.gameName= gameName
        self.modeLst= modeLst + ["help"]
        self.mode= modeLst[0]
        self.prmDsc= parameters
        self.parameters= { p:self.prmDsc[p][1] for p in self.prmDsc }
        self.optDsc= options
        self.options= { p:False for p in self.optDsc }
        self.interpret()

    # Accessor:
    def option(self, o):
        return self.options[o]
    
    def parameter(self, p):
        return self.parameters[p]

    def interpret(self):
        shArgs= sys.argv
        self.cmd= shArgs.pop(0)
        while len(shArgs) != 0 :
            v= shArgs.pop(0)
            if v[0] == '-' :
                if not self.interpretParam(v, shArgs ) :
                    print( "/!\ invalid parameters ")
                    self.mode= "help"
            elif v in self.modeLst :
                if self.mode != "help" :
                   self.mode= v
            else :
                print( "/!\ unknown mode "+ v )
                self.mode= "help"
        if self.mode == "help" :
            print( self.help() )

    def interpretParam( self, params, shArgs ):
        ok= True
        for p in params[1:-1] :
            if p in self.optDsc :
                self.options[p]= True
            else :
                ok= False

        p= params[-1]
        if p in self.prmDsc :
            self.parameters[p]= shArgs.pop(0)
        elif p in self.optDsc :
            self.options[p]= True
        else :
            ok= False

        return ok

    # print:
    def __str__(self):
        s= f"{self.cmd} {self.gameName} (mode: {self.mode}"
        for op in self.options :
            if self.options[op] :
                s+= ", "+ self.optDsc[op][0]
        for pa in self.parameters :
            s+= f", {self.prmDsc[pa][0]}: {self.parameters[pa]}" 
        return s+")"

    def help(self):
        help= f"{self.gameName} {self.cmd} command : {self.cmd} [options/parameters] mode OR `{self.cmd} help` (to get this help)"
        help+= f"\n  Example: python3 {self.cmd} {self.modeLst[0]}"
        help+= f"\n  Modes: [{ ', '. join(self.modeLst) }]"
        help+= "\n  Options:"
        for op in self.optDsc :
            help += f"\n     -{op} : {self.optDsc[op][0]}"
        help+= "\n  Parameters:"
        for p in self.prmDsc :
            help += f"\n     -{p} : {self.prmDsc[p][0]} (default: {self.prmDsc[p][1]})"
        return help
