#read the instructions from the file and parse them
# Path: reader.py
class Reader:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(self.filename, 'r',newline='')
        self.lines = []
        for line in self.file:
            self.lines.append(line.strip())
        self.file.close()
        self.ins_memory = self.parse_instructions()
    #self.line[]=["lw $2,8($0)", "lw $3,16($0)]
    # parse the instructions 
    def parse_instructions(self):
        # parse the instructions
        instructions = []
        for line in self.lines:
            # split the line
            line = line.split()
            # get the instruction
            instruction = line[0]
            # get the rest of the line
            rest = line[1]
            # add the instruction and the rest to the instructions
            instructions.append([instruction, rest])
        # return the instructions
        return instructions
    
    def get_ins_memory(self):
        return self.ins_memory
    # for i in range(len(ins_memory)):
    #     print(ins_memory[i][0]) #instruction