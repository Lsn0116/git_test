# $0~$31
# $0 is always 0,another is 1 (32 bits)
# memory is w0 to w31, each size is word and value is 1
class RegisterFile:
    def __init__(self):
        self.register_values = {}
        self.register_names = ['$0','$1','$2','$3','$4','$5','$6','$7','$8','$9','$10','$11','$12','$13','$14','$15','$16','$17','$18','$19','$20','$21','$22','$23','$24','$25','$26','$27','$28','$29','$30','$31']
        self.initialize_register_values()
        
    def initialize_register_values(self):
        for i in range(1,32):
            self.register_values[self.register_names[i]] = 1
        self.register_values[self.register_names[0]] = 0
    
    def get_register_value(self, register_name):
        return self.register_values[register_name]
    
    def set_register_value(self, register_name, register_value):
        if register_name != '$0':
            self.register_values[register_name] = register_value

    def print_register_values(self,filename):
        f = open(filename,'a')
        f.write('\n\n')
        for i in range(32):
            print(self.register_names[i] +': '+ str(self.register_values[self.register_names[i]]))
            f.write(self.register_names[i] +': '+ str(self.register_values[self.register_names[i]])+'\n')
        f.close()

class Memory:
    def __init__(self,ins_memory):
        self.data_memory = {}
        self.instruction_memory = []
        self.initialize_data_memory()
        self.initialize_instruction_memory(ins_memory)
        
    def initialize_data_memory(self):
        for i in range(32):
            self.data_memory['w'+str(i)] = 1
    def initialize_instruction_memory(self,ins_memory):
        self.instruction_memory = ins_memory
    def get_data_memory(self,i):
        return self.data_memory[i]
    
    def get_ins_memory(self,i):
        return self.instruction_memory[i]
    
    def set_data_memory(self, address, value):
        self.data_memory[address] = value
    
    def print_data_memory(self,filename):
        f = open(filename,'a')
        f.write('\n\n')
        for i in range(32):
            print('w'+str(i)+': '+str(self.data_memory['w'+str(i)]))
            f.write('w'+str(i)+': '+str(self.data_memory['w'+str(i)])+'\n')
        f.close()

    def get_all_ins_memory(self):
        return self.instruction_memory
    def get_data_memory_withW(self,i):
        return self.data_memory[i]