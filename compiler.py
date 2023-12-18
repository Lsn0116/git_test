import registers_N_memories as rnm
#control the datapath and the pipeline stages
#fetch
#decode (hazard detection unit)(let pipeline register clear the control signals and IF/IDWrite = 0)
#execute(check forwading here if needed(EX/MEM.rd =ID/EX.rs or rt))
#memory(check forwarding here if needed(MEM/WB.rd =ID/EX.rs or rt)and not (EX/MEM.rd =ID/EX.rs or rt))
#writeback

#while loop for each cycle (until all instructions are finished)
#if each stage is empty then break
#for loop for each stage: (from writeback to fetch) (one cycle)
    #find the oldest instruction in the pipeline
    #if there is no instruction then fetch the first instruction   
    #each stage would check the pipeline register and control signals to see what to do
    #if ID/EX pipeline register is empty then do nothing
    #if IF/IDWrite = 0 then do not fetch the next instruction 
    #(actually refetch the next instruction, but do not write it to IF/ID pipeline register)

class Compiler:
    def __init__(self, ins_memory):
        self.register_file = rnm.RegisterFile()
        self.memory = rnm.Memory(ins_memory)
        self.PC = 0
        self.instructions = []
        self.data = []
        self.labels = {}
        self.compile()
        self.data_memory = self.memory.get_data_memory()
        self.instruction_memory = self.memory.get_instruction_memory()
        self.register_values = self.register_file.get_register_values()
        self.instructions = self.instructions
        self.data = self.data
        self.labels = self.labels
        self.PC = self.PC

    def compile(self):
        #compile the instructions
        for i in range(len(self.memory.get_instruction_memory())):
            #get the instruction
            instruction = self.ins_memory[i][0]
            #get the rest of the line
            rest = self.ins_memory[i][1]
            #check if the instruction is a label
            if instruction[-1] == ':':
                #add the label to the labels
                self.labels[instruction[:-1]] = self.PC
            else:
                #add the instruction to the instructions
                self.instructions.append([instruction, rest])
                #increment the PC
                self.PC += 4
        #compile the data
        for i in range(len(self.ins_memory)):
            #get the instruction
            instruction = self.ins_memory[i][0]
            #get the rest of the line
            rest = self.ins_memory[i][1]
            #check if the instruction is a label
            if instruction[-1] == ':':
                #do nothing
                pass
            elif instruction == '.word':
                #add the data to the data
                self.data.append(rest[0])
                #increment the PC
                self.PC += 4
            else:
                #do nothing
                pass