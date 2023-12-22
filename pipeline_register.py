# class PipelineRegister:
# data(values)
# registers
# control signals
# instruction name
# write (write to the pipeline register)
class PipelineRegister:
    def __init__(self):
        self.name = ""  # name of instruction
        self.data: int  # data values
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

    def set_control_signals(self, control_signals):
        self.control_signals = control_signals

    def set_registers(self, registers):
        self.registers = registers

    def set_write(self, write):
        self.write = write

    def get_write(self):
        return self.write

    # each stage may need to remove the control signals that it already need
    def remove_control_signals(self, control_signals):
        del self.control_signals[control_signals]

    def add_data(self, key, value):
        self.data[key] = value

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
    def set_stall(self):
        self.stall = 1
    
    def get_stall(self):
        return self.stall
    
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

