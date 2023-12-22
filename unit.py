import pipeline_register as pr

#a class to simulate the control unit 
class ControlUnit:
    
    def __init__(self):
        self.RegDst:str = '0'
        self.ALUSrc:str = '0'
        self.Branch:str = '0'
        self.MemRead:str = '0'
        self.MemWrite:str = '0'
        self.RegWrite:str = '0'
        self.MemToReg:str = '0'

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
#check fowarding
class HazardDetectionUnit:
    
    def __init__(self):
        self.rs = ''
        self.rt = ''
        self.rd = ''
        self.last_rd = '' #ID/EX.rd
        self.last_rt = '' #ID/EX.rt
        self.second_last_rd = '' #EX/MEM.rd
        self.second_last_rt = '' #EX/MEM.rt
    #----new def----------
    '''def initialize_last_ins(self):
        
    def initialize_second_last_ins(self):

    def checkHazard(self):
    '''



class ForwardingUnit:
    #in ID stage

    def __init__(self):
        '''self.this_instruction:pr.PipelineRegister
        self.last_instruction:pr.PipelineRegister
        self.second_last_instruction:pr.PipelineRegister
        self.rs =''
        self.rt =''
        self.last_rd=''
        self.last_rt=''
        self.second_last_rd='' 
        self.second_last_rt='''''
        self.ins_name = ''
        self.last_name = ''
        self.second_last_name = ''
        self.rt = ''
        self.rs = ''
        self.last_rd = ''
        self.last_rt = ''
        self.second_last_rd = ''
        self.second_last_rt = ''
        self.forwarding_type =''
    
    
    def set(self, this_instruction:pr.PipelineRegister, last_instruction:pr.PipelineRegister, second_last_instruction:pr.PipelineRegister):
        self.ins_name = this_instruction.get_name()
        self.rt = this_instruction.get_one_register('rt')
        self.rs = this_instruction.get_one_register('rs')
        self.last_rd = last_instruction.get_one_register('rd')
        self.last_rt = last_instruction.get_one_register('rt')
        self.second_last_rd = second_last_instruction.get_one_register('rd')
        self.second_last_rt = second_last_instruction.get_one_register('rt')

    def checkForwarding(self):
    #check rd is the same as ID/EX.rt or ID/EX.rs and EX/MEM.rt or EX/MEM.rs
    #if yes then forward(replace the value of the register with the value in the pipeline register)
    
        #R-format
        #forwarding type:(EX_rt:從EX/MEM讀取data給rt,EX_rs:從EX/MEM讀取data給rs, MEM_rt:從MEM/WB讀取data給rt, MEM_rs:從MEM/WB讀取data給rs)
        if(self.ins_name == 'add' or self.ins_name == 'sub'):
            
            if(self.rt==self.last_rd):
                self.forwarding_type = 'EX_rt' #EX hazrad
            elif(self.rs==self.last_rd):
                self.forwarding_type='EX_rs'
            elif(self.rt==self.second_last_rd):
                self.forwarding_type = 'MEM_rt' #MEM hazrad
            elif(self.rs==self.second_last_rd):
                self.forwarding_type = 'MEM_rs'
            else:
                print("no forwarding")

        #I-format
        elif(self.ins_name == 'lw' or self.ins_name == 'sw'):
            if(self.rt==self.last_rd):
                self.forwarding_type = 'EX_rt'
            elif(self.rt==self.second_last_rd):
                self.forwarding_type = 'MEM_rt'
            else:
                print("no forwarding")

    def checkForwarding_branch(self):
         if(self.ins_name == 'beq'):
            if(self.rt==self.last_rd):
                self.forwarding_type = 'EX_rt' #EX hazrad
            elif(self.rs==self.last_rd):
                self.forwarding_type='EX_rs'
            elif(self.rt==self.second_last_rd):
                self.forwarding_type = 'MEM_rt' #MEM hazrad
            elif(self.rs==self.second_last_rd):
                self.forwarding_type = 'MEM_rs'
            else:
                print("no forwarding")


            
    