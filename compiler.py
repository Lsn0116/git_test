import registers_N_memories as rnm
import pipeline_register as pr
import unit
#control the datapath and the pipeline stages
#fetch
#decode
'''
(let pipeline register clear the control signals and IF/IDWrite = 0)
(check forwading here if needed(EX/MEM.rd =ID/EX.rs or rt))
(check forwarding here if needed(MEM/WB.rd =ID/EX.rs or rt)and not (EX/MEM.rd =ID/EX.rs or rt))
'''
#execute
#memory
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
        
        self.data_memory = self.memory.get_data_memory()
        # self.instruction_memory = self.memory.get_instruction_memory()
        # self.register_values = self.register_file.get_register_values()
        self.pipeline_registers = {'IF/ID': pr.PipelineRegister(), 'ID/EX': pr.PipelineRegister(), 'EX/MEM': pr.PipelineRegister(), 'MEM/WB': pr.PipelineRegister()}
        # self.control_unit = unit.ControlUnit()
        # self.hazard_detection_unit = unit.HazardDetectionUnit()
        # self.forwarding_unit = unit.ForwardingUnit()
        # self.PC_word = 0
        self.compile()

    def compile(self):
        #compile the instructions until finished the all instructions
        self.pipeline_registers['IF/ID'].set_name(self.memory.get_instruction_memory(self.PC_word)[0])
        print(self.pipeline_registers['IF/ID'].name)

        while(self.PC_word < len(self.memory.get_instruction_memory())):
            #WB stage
            #MEM stage
            #EX stage
            #ID stage
            #IF stage
            pass

        return
    '''you may need some functions to help you to do the pipeline stages, add these to the pipeline register class (def xxxx(): )'''
    def IF_stage(self):
        self.pipeline_registers['IF/ID'].set_name(self.instruction_memory[self.PC_word][0])
        #fetch the instruction from the instruction memory
        #increment the PC (word) if IF/IDWrite = 1, if IF/IDWrite = 0 then do not fetch the next instruction
        #spilt the instruction into the instruction name and the rest of the line (include registers)
        #add these information to the IF/ID pipeline register (use dict to store the registers and control signals)

        '''i used to write this code, may can use it in this stage'''
        # #compile the instructions (may can use in IF stage)
        # for i in range(len(self.memory.get_instruction_memory())):
        #     #get the instruction
        #     instruction = self.ins_memory[i][0]
        #     #get the rest of the line
        #     rest = self.ins_memory[i][1]
        #     #add the instruction to the instructions
        #     self.instructions.append([instruction, rest])
        #     #increment the PC (word)
        #     self.PC_word += 1
        if not self.pipeline_registers['ID/EX'].control_signals.get('Branch'):
            instruction = self.memory.get_instruction_memory(self.PC_word)
            self.pipeline_registers['IF/ID'].set_name(instruction[0])
            # Update PC only if IF/IDWrite is 1
            if self.pipeline_registers['IF/ID'].control_signals.get('IF/IDWrite'):
                self.PC_word += 1
        pass

    def ID_stage(self):
        #decide the control signals for the ID/EX pipeline register
        #read data from the register file, and store the data to the ID/EX pipeline register(if not stall and not forwarding and *branch?*)
        #dazard detection unit
        #forwarding unit
        #check RegDst(use the data self.control_unit.get_control_signals())
        #check forwading here if needed, replace the value of the register with the value in the pipeline register(EX/MEM or MEM/WB)
        self.control_unit.set_control_signals(self.pipeline_registers['IF/ID'].name)
        C_S = self.control_unit.get_control_signals()
        self.pipeline_registers['ID/EX'].set_control_signals(C_S)
        #check branch (PC adder and reg compare(use the data stored in the pipeline register))
        pass
    
    def EX_stage(self):
        #check ALUSrc
        #calculate the ALU result
        #add the ALU result to the EX/MEM pipeline register
        pass

    def MEM_stage(self):
        if self.pipeline_registers['EX/MEM'].write:
            takeBranch = self.pipeline_registers['EX/MEM'].control_signals.get('Branch')
            memRead = self.pipeline_registers['EX/MEM'].control_signals.get('MemRead')
            memWrite = self.pipeline_registers['EX/MEM'].control_signals.get('MemWrite')
            aluResult = self.pipeline_registers['EX/MEM'].data.get('ALUResult')
            destRegister = self.pipeline_registers['EX/MEM'].registers.get('DestinationRegister')

            if takeBranch and aluResult == 0:
                self.PC_word = self.pipeline_registers['EX/MEM'].data.get('BranchTarget')

            if memRead:
                read_address = aluResult
                self.pipeline_registers['MEM/WB'].data['ReadData'] = self.memory.get_data_memory(read_address)

            if memWrite:
                write_address = aluResult
                write_data = self.pipeline_registers['EX/MEM'].data.get('WriteData')
                self.memory.set_data_memory(write_address, write_data)

            self.pipeline_registers['MEM/WB'].registers['DestinationRegister'] = destRegister

        self.pipeline_registers['EX/MEM'].write = 0
        self.pipeline_registers['EX/MEM'].data.clear()
        self.pipeline_registers['EX/MEM'].registers.clear()
        self.pipeline_registers['EX/MEM'].control_signals.clear()

        self.MEM_over = True

        pass

    def WB_stage(self):
        #check pipleline register MEM/WB can write or not
        if self.pipeline_registers['MEM/WB'].write:
            #get the data from the pipeline register that already calculated
            data_to_write = self.pipeline_registers['MEM/WB'].get_data()
            if data_to_write is not None and self.pipeline_registers['MEM/WB'].control_signals.get('RegWrite'):
                destination_register = self.pipeline_registers['MEM/WB'].registers.get('DestinationRegister')
                self.register_file.set_register_value(destination_register, data_to_write)

        self.pipeline_registers['MEM/WB'].write = 0
        self.pipeline_registers['MEM/WB'].data.clear()
        self.pipeline_registers['MEM/WB'].registers.clear()
        self.pipeline_registers['MEM/WB'].control_signals.clear()

        self.WB_over = True
        pass

