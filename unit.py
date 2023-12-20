import pipeline_register as pr
#a class to simulate the control unit 
class ControlUnit:
    
    def __init__(self):
        RegDst:str = '0'
        ALUSrc:str = '0'
        Branch:str = '0'
        MemRead:str = '0'
        MemWrite:str = '0'
        RegWrite:str = '0'
        MemToReg:str = '0'

    def set_control_signals(self, instruction):
        if instruction == 'lw':
            self.ALUSrc = '1'
            self.MemRead = '1'
            self.RegWrite = '1'
            self.MemToReg = '1'
        elif instruction == 'sw':
            self.RegDst = 'X'
            self.MemToReg = 'X'
            self.ALUSrc = '1'
            self.MemWrite = '1'
        elif instruction == 'add':
            self.RegDst = '1'
            self.RegWrite ='1'
        elif instruction == 'sub':
            self.RegDst = '1'
            self.RegWrite = '1'
        elif instruction == 'beq':
            self.Branch = '1'
            self.RegDst = 'X'
            self.MemToReg = 'X'

    def get_control_signals(self):
        return {'RegDst':self.RegDst,'ALUSrc':self.ALUSrc, 'Branch':self.Branch, 'MemRead':self.MemRead, 'MemWrite':self.MemWrite, 'RegWrite':self.RegWrite, 'MemToReg':self.MemToReg}


#a class to simulate the hazard detection unit
#check if the instruction need to be stall (lw, sw, beq)
#check the last and second last instruction in the pipeline
class HazardDetectionUnit:
    
    def __init__(self):
        self.rs = ''
        self.rt = ''
        self.rd = ''
        self.last_rd = '' #ID/EX.rd
        self.last_rt = '' #ID/EX.rt
        self.second_last_rd = '' #EX/MEM.rd
        self.second_last_rt = '' #EX/MEM.rt


class ForwardingUnit:
    #in ID stage

    def __init__(self,this_instruction:pr.PipelineRegister(), last_instruction:pr.PipelineRegister(), second_last_instruction:pr.PipelineRegister()):
        self.this_instruction = this_instruction
        self.last_instruction = last_instruction
        self.second_last_instruction = second_last_instruction
        self.rs = this_instruction.registers['rs']
        self.rt = this_instruction.registers['rt']
        self.last_rd = last_instruction.registers['rd']
        self.last_rt = last_instruction.registers['rt']
        self.second_last_rd = second_last_instruction.registers['rd']
        self.second_last_rt = second_last_instruction.registers['rt']
        
    
    def checkForwarding(self):
    #check rd is the same as ID/EX.rt or ID/EX.rs and EX/MEM.rt or EX/MEM.rs
    #if yes then forward(replace the value of the register with the value in the pipeline register)
        if(self.second_last_rd!='' and (self.last_rd == self.rs or self.last_rd == self.rt)):
            return True    
        elif(self.last_rt != '' and (self.last_rt == self.rs or self.last_rt == self.rt)):
            return True
        elif(self.second_last_rd != '' and (self.second_last_rd == self.rs or self.second_last_rd == self.rt)):
            return True
        elif(self.second_last_rt != '' and (self.second_last_rt == self.rs or self.second_last_rt == self.rt)):
            return True
        
        