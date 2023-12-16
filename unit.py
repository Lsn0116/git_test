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
        return [self.RegDst, self.ALUSrc, self.Branch, self.MemRead, self.MemWrite, self.RegWrite, self.MemToReg]


#a class to simulate the hazard detection unit
class HazardDetectionUnit:
    
    def __init__(self):
        self.control_signals = ""
        self.ID_EX_registers = ""
        self.EX_MEM_registers = ""
        self.MEM_WB_registers = ""
        self.forwarding = ""
        self.stalling = ""
        self.branch = ""

    def set_control_signals(self, control_signals):
        self.control_signals = control_signals

    def set_ID_EX_registers(self, ID_EX_registers):
        self.ID_EX_registers = ID_EX_registers

    def set_EX_MEM_registers(self, EX_MEM_registers):
        self.EX_MEM_registers = EX_MEM_registers

    def set_MEM_WB_registers(self, MEM_WB_registers):
        self.MEM_WB_registers = MEM_WB_registers

    def set_forwarding(self, forwarding):
        self.forwarding = forwarding

    def set_stalling(self, stalling):
        self.stalling = stalling

    def set_branch(self, branch):
        self.branch = branch

    def get_control_signals(self):
        return self.control_signals

    def get_ID_EX_registers(self):
        return self.ID_EX_registers

    def get_EX_MEM_registers(self):
        return self.EX_MEM_registers

    def get_MEM_WB_registers(self):
        return self.MEM_WB_registers

    def get_forwarding(self):
        return self.forwarding

    def get_stalling(self):
        return self.stalling

    def get_branch(self):
        return self.branch