#class PipelineRegister:
#data(values)
#registers
#control signals
#instruction name
#write (write to the pipeline register)
class PipelineRegister:

    def __init__(self):
        self.name = "" #name of instruction
        self.data = "" #data values
        self.control_signals = "" #control signals
        self.registers = "" #registers
        self.write = 1 #write to the pipeline register 1 = yes, 0 = no