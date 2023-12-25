# class PipelineRegister:
# data(values)
# registers
# control signals
# instruction name
# write (write to the pipeline register)
import registers_N_memories as rnm
class PipelineRegister:
    def __init__(self):
        self.name = ""  # name of instruction
        self.data: int | str  = 1 # data values
        self.control_signals = {}  # control signals
        self.registers = {}  # registers
        self.write = 1  # write to the pipeline register 1 = yes, 0 = no
        self.stall = 0

    def set_name(self, name):
        self.name = name
    
    def get_name(self):
        return self.name

    def set_data(self, data):
        self.data = data
    
    def get_data(self):
        return self.data

    def set_control_signals(self, control_signals):
        self.control_signals = control_signals

    def set_registers(self, registers):
        self.registers = registers

    def set_write(self, write):
        self.write = write

    def get_write(self):
        return self.write

    # each stage may need to remove the control signals that it already need
    def remove_control_signals(self, control_signals:list):
        for signal in control_signals:
            if signal in self.control_signals:
                 del self.control_signals[signal]

    def set_data(self, data):
        self.data = data

    def get_register(self):
        return self.registers

    def get_one_register(self, i):
        if i in self.registers:
            return self.registers[i]
        else:
            return None
    #-------new def------------------
    def get_control_signals(self):
        return self.control_signals
    def get_data(self):
        return self.data
    
    def get_one_control_signals(self, i):
        if i in self.control_signals:
            return self.control_signals[i]
        else:
            return None
    def clear(self):
        self.name = ""
        self.data = 0
        self.control_signals = {}
        self.registers = {}
        self.write = 1
        self.stall = 0
    def IsEmpty(self):
        if self.name == "":
            return True
        else:
            return False
    

  

    def set_stall(self):
        self.stall = 1
    
    def get_stall(self):
        return self.stall
    
    def clear(self):
        self.name = ""
        self.data = 1
        self.control_signals = {}
        self.registers = {}
        self.write = 1
        self.stall = 0
    def IsEmpty(self):
        if self.name == "":
            return True
        else:
            return False
    def print_register(self):
        print("name: ", self.name)
        if self.control_signals != {}:
            print("data: ", self.data)
        print("control_signals: ", self.control_signals)
        print("registers: ", self.registers)
        print("write: ", self.write)
        print("stall: ", self.stall)