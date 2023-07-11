
from numpy import linspace
from numpy import float64
from numpy import power, exp, log10, log2, log
from colorama import Fore

class SeriesStr:
    '''Guidelines for Command writing:\n
        1. All characters will be converted to lower case.\n
        2. Use comma separated string to represent string list.\n
        3. Inner-Repeat is ONLY used for CW_SWEEP: MUST use EXACTLY ' r ' (in order to differentiate from r inside word-string).\n
        4. waveform.inner_repeat: the repeat-counts indicated after the ' r ' or '^', determining how every .data's element will be repeated.\n
        5. Option to let waveform be 'function-ized' using f: <base/power/log..> at the end of the command/ order:
            a. Base: data points from dense to sparse.
            b. Power: 0-1: same with Log, >1: same with Base, but slower.
            c: Log: data points from sparse to dense.
        NOTE: '^' is equivalent to ' r ' without any spacing restrictions.
    '''
    def __init__(self, command):
        # defaulting to lower case
        command = str(command)
        self.command = command.lower()

        # special treatment to inner-repeat command: (to extract 'inner_repeat' for cwsweep averaging)
        self.inner_repeat = 1
        if ' r ' in self.command:
            self.command, self.inner_repeat = self.command.split(' r ')
            while " " in self.inner_repeat: self.inner_repeat = self.inner_repeat.replace(" ","")
            self.inner_repeat = int(self.inner_repeat)
        if '^' in self.command:
            self.command, self.inner_repeat = self.command.split('^')
            while " " in self.inner_repeat: self.inner_repeat = self.inner_repeat.replace(" ","")
            self.inner_repeat = int(self.inner_repeat)

        # correcting back ("auto-purify") the command-string after having retrieved the repeat-count or not:
        # get rid of multiple spacings
        while " "*2 in self.command:
            self.command = self.command.replace(" "*2," ")
        # get rid of spacing around keywords
        while " *" in self.command or "* " in self.command:
            self.command = self.command.replace(" *","*")
            self.command = self.command.replace("* ","*")
        while " to" in self.command or "to " in self.command:
            self.command = self.command.replace(" to","to")
            self.command = self.command.replace("to ","to")
        while " (" in self.command or "( " in self.command:
            self.command = self.command.replace(" (","(")
            self.command = self.command.replace("( ","(")
        while " )" in self.command or ") " in self.command:
            self.command = self.command.replace(" )",")")
            self.command = self.command.replace(") ",")")
        while " f" in self.command or "f " in self.command:
            self.command = self.command.replace(" f","f")
            self.command = self.command.replace("f ","f")
        while " :" in self.command or ": " in self.command:
            self.command = self.command.replace(" :",":")
            self.command = self.command.replace(": ",":")
        while " /" in self.command or "/ " in self.command:
            self.command = self.command.replace(" /","/")
            self.command = self.command.replace("/ ","/")
        # print(Fore.CYAN + "Command: %s" %self.command)
        
        command = self.command.split(" ") + [""]
        
        # 1. building string list:
        if ("," in command[0]) or ("," in command[1]):
            # remove all sole-commas from string list command:
            command = [x for x in command if x != ',']
            # remove all attached-commas from string list command:
            command = [i for x in command for i in x.split(',') if i != '']
            self.data = command
            self.count = len(command)
        # 2. building number list:
        else:
            command = [x for x in command if x != ""]
            self.data, self.count = [], 0
            for cmd in command:
                self.count += 1
                if "*" in cmd and "to" in cmd:
                    C = [j for i in cmd.split("*") for j in i.split('to')]
                    try:
                        start = float(C[0])
                        steps = range(int(len(C[:-1])/2))
                        for i, target, asterisk in zip(steps,C[1::2],C[2::2]):
                            num = asterisk.split("f:")[0]
                            self.count += int(num)
                            # 2a. Simple linear space / function:
                            self.data += list(linspace(start, float(target), int(num), endpoint=False, dtype=float64))
                            if i==steps[-1]: 
                                self.data += [float(target)] # data assembly complete
                                # 2b. Customized space / function for the WHOLE waveform: base, power, log scales
                                if "f:" in asterisk:
                                    func = asterisk.split("f:")[1]
                                    # print(Fore.CYAN + "Function: %s" %func)
                                    if 'base' in func:
                                        if "e" == func.split('/')[1]: self.data = list(exp(self.data))
                                        else: self.data = list(power(float(func.split('/')[1]), self.data))
                                    elif 'power' in func:
                                        self.data = list(power(self.data, float(func.split('/')[1])))
                                    elif 'log10' in func:
                                        self.data = list(log10(self.data))
                                    elif 'log2' in func:
                                        self.data = list(log2(self.data))
                                    elif 'log' in func:
                                        self.data = list(log(self.data))
                                    else: print(Fore.RED + "Function NOT defined YET. Please consult developers")
                                    print(Fore.YELLOW + "scaled %s points" %len(self.data))
                            else: 
                                start = float(target)
                    except: # rooting out the wrong command:
                        # raise
                        print("Invalid command")
                        pass
                else: self.data.append(float(cmd))     

