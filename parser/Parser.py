import re

class Parser:
    def __init__(self):
        self.__output_code = ""
        self.__input_code = ""

        self.__keyList = []
        self.__inits = ""

    def __checkIndent(self, string):
        ''' returns a number of spaces before a line '''
        index = 0
        while index < len(string) and string[index] == ' ':
            index += 1
        return index

    def __addInit(self):
        ''' initializes dictionary '''
        self.__inits = "lines_dict = {n : 0 for n in " + str(self.__keyList) + "}\n"

    def __addLineVars(self):
        ''' this method must be rewritten '''
        lineNum = 1
        self.__output_code += self.__input_code.split('\n')[0] + '\n'
        for line in self.__input_code.split('\n')[1:]:
            lineNum += 1
            spaceNum = self.__checkIndent(line)

            if re.match(r'\s*#', line) != None or re.fullmatch(r'\s*', line) or re.match(r' *else:', line) != None:
                self.__output_code += (line + '\n')
                continue
            elif re.match(r'\s*except ', line) != None:
                self.__output_code += (line + '\n')
                self.__output_code += (''.join([" " for _ in range(spaceNum + 4)]) + "lines_dict[" + str(lineNum) + "] += 1\n")
                self.__keyList.append(lineNum)
            else:
                self.__output_code += (''.join([" " for _ in range(spaceNum)]) + "lines_dict[" + str(lineNum) + "] += 1\n")
                self.__output_code += (line + '\n')
                self.__keyList.append(lineNum)

    def __readAlgoFromFile(self, filename):
        algo = ""
        with open(filename, 'r') as f:
            for line in f.readlines():
                algo += line
        return algo

    def __saveAlgoToFile(self, output, filename):
        with open(filename, 'w') as f:
            for line in output.split("\n"):
                f.write(line + "\n")

    def parseCode(self, fileFrom, fileTo):
        ''' reads input, build output and saves output '''
        self.__input_code = self.__readAlgoFromFile(fileFrom)

        self.__addLineVars()
        self.__addInit()

        output = self.__inits + self.__output_code

        self.__saveAlgoToFile(output, fileTo)
    