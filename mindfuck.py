import sys

class Mindfuck:

    def __init__(self, code, ascii = True, trace = False):
        self.code = code
        self.dataLimit = 30000
        self.data = self.getFreshData()
        self.name = ''
        self.pointer = 0
        self.ascii = ascii
        self.trace = trace
        self.output = ''

    def getFreshData(self):
        return [0 for x in range(self.dataLimit)]

    def run(self):
        skipper = None
        idx = 0
        while idx < len(self.code):
            if skipper != None: # skipping up to and over skipperIdx
                idx = skipper+1
                skipper = None
                continue

            line = self.code[idx]
            if self.trace:
                self.tracePrint(line)
            lineResponse = self.exeLine(line, idx)

            if type(lineResponse) == int:
                skipper = lineResponse # skip to idx given in lineResponse
            elif lineResponse == True:
                idx += 1 # normal response
            else:
                print('err lineResponse: ' + lineResponse + ' on index: ' + idx) # failed response, shouldnt get here unless syntax is fucked
                sys.exit()

        print('Out: ' + self.output)

    def exeLine(self, line, idx):
        if line == '>':
            self.pointer+=1
            self.pointerRangeCheck()

        elif line == '<':
            self.pointer-=1
            self.pointerRangeCheck()

        elif line == '+':
            self.data[self.pointer]+=1
            self.dataValueRangeCheck()

        elif line == '-':
            self.data[self.pointer]-=1
            self.dataValueRangeCheck()

        elif line == '.':
            val = self.data[self.pointer]
            if self.ascii:
                val = chr(val)
            else:
                val = str(val) + ' ' # if not ascii space out the output

            print(val) # TODO check for function to run instead
            self.output = self.output + val

        elif line == ',':
            inVal = input('input decimal: ')
            try:
                inVal = int(inVal)
            except ValueError:
                print("That's not an int!")
                sys.exit()
            self.data[self.pointer] = inVal
            self.dataValueRangeCheck()

        elif line == '[':
            if self.data[self.pointer] == 0:
                # if zero jump to end of loop, else ignore
                return idx + self.getBlockContentEndIdx(self.code[idx:],'[',']')

        elif line == ']':
            if self.data[self.pointer] != 0:
                # if not zero jump to start of loop
                return self.getBlockContentStartIdx(self.code[:idx+1],'[',']')

        elif line == '#':
            jumpTo = False
            try:
                jumpTo = self.code.index('\n', idx+1) # find first occourance of \n after idx and skip over it
            except ValueError:
                return len(self.code) # couldn't find end of line, which means that we must skip the rest of the code
            return jumpTo

        elif line == '/':
            jumpTo = False
            try:
                jumpTo = self.code.find('/', idx+1) # find first occourance of / after idx and skip over it
            except ValueError:
                print('couldn\'t find end of area comment, index: ' + idx)
                sys.exit()
            return jumpTo

        elif line == '@':
            self.pointer = self.data[self.pointer]

        elif line == '~':
            self.data = self.getFreshData()

        elif line == '*':
            self.name = self.name + chr(self.data[self.pointer])

        elif line == '!':
            self.name = ''

        elif line == ';':
            ch = False
            try:
                f = open(self.name)
                txt = f.read()
                ch = ord(txt[self.data[self.pointer]])
            except: # if errors finding file, finding index, or converting ascii -> decimal we set to zero
                ch = 0

            self.data[self.pointer] = ch

        elif line == ':':
            with open(self.name, "a") as file:
                file.write(chr(self.data[self.pointer]))

        elif line == '?':
            f = open(self.name)
            txt = f.read()
            self.code = self.code[:idx] + txt + self.code[1+idx:] # replace ? with code from file
            return idx-1 # move back a slot so we next run the character which is now where ? was and continue from there

        elif line == '^':
            return len(self.code) #  ends execution by setting skipper to end

        elif line == '\n' or line == ' ': # we skip over newlines and spaces
            pass

        else:
            return False


        return True

    def getBlockContentEndIdx(self, str, blockOpen, blockClose):
        if str[0] != blockOpen:
            print('provided block must start with: [')
            sys.exit()
        counter = 0
        for idx, line in enumerate(str):
            if line == blockOpen:
                counter+=1
            elif line == blockClose:
                counter-=1

            if counter == 0:
                return idx

        return False

    def getBlockContentStartIdx(self, str, blockOpen, blockClose):
        str = str[::-1]
        if str[0] != blockClose:
            print('provided block must end with: ]')
            sys.exit()
        counter = 0
        for idx, line in enumerate(str):
            if line == blockClose:
                counter+=1
            elif line == blockOpen:
                counter-=1

            if counter == 0:
                return len(str) - (idx+1) # reversed string so take away from len +1 to place index value on other side of char

        return False

    def pointerRangeCheck(self):
        if (self.pointer < 0 or self.pointer > self.dataLimit-1):
            print('pointer out of bounds')
            sys.exit()

    def dataValueRangeCheck(self): # within 16 bits
        if self.data[self.pointer] < 0:
            self.data[self.pointer] += 0x100
        elif self.data[self.pointer] > 0xff:
            self.data[self.pointer] -= 0x100

    def tracePrint(self, line):
        nonZeroIdxs = [i for i, e in enumerate(self.data) if e != 0]
        finalIdx = None
        try:
            finalIdx = nonZeroIdxs[-1]
        except IndexError:
            pass
        if finalIdx == None or finalIdx < 5:
            finalIdx = 5

        print('# ' + str( self.data[:finalIdx]) ) # prints shortened version of self.data
        pointStr = '#  '
        for i in range(self.pointer):
            pointStr = pointStr + '   '

        print(pointStr + '^')
        print('next line: ' + line)


args = sys.argv
args.pop(0)
code = ''
if (len(args) > 1):
    print('expected a maximum of 1 argument')
    sys.exit()
elif (len(args) < 1):
    code = input('If you wish to execute a file then cancel this execution and pass the filename as an argument.\nOr paste your code here: ')
else:
    with open(args[0], 'r') as myfile:
        code=myfile.read()

ascii = input('Want output as ascii or decimal: ')
if ascii == 'ascii':
    ascii = True
elif ascii == 'decimal':
    ascii = False
else:
    print('Invalid input: ' + ascii)
    sys.exit()

trace = input('Turn on trace: ')
if trace == 'yes':
    trace = True
elif trace == 'no':
    trace = False
else:
    print('Invalid input: ' + trace)
    sys.exit()

Mindfuck(code, ascii, trace).run()
