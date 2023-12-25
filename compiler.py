import registers_N_memories as rnm
import pipeline_register as pr
import unit

# control the datapath and the pipeline stages
# fetch
# decode
"""
(let pipeline register clear the control signals and IF/IDWrite = 0)
(check forwading here if needed(EX/MEM.rd =ID/EX.rs or rt))
(check forwarding here if needed(MEM/WB.rd =ID/EX.rs or rt)and not (EX/MEM.rd =ID/EX.rs or rt))
"""
# execute
# memory
# writeback

# while loop for each cycle (until all instructions are finished)
# if each stage is empty then break
# for loop for each stage: (from writeback to fetch) (one cycle)
# find the oldest instruction in the pipeline
# if there is no instruction then fetch the first instruction
# each stage would check the pipeline register and control signals to see what to do
# if ID/EX pipeline register is empty then do nothing
# if IF/IDWrite = 0 then do not fetch the next instruction
# (actually refetch the next instruction, but do not write it to IF/ID pipeline register)


class Compiler:
    def __init__(self, ins_memory):
        
        self.register_file = rnm.RegisterFile()
        self.memory = rnm.Memory(ins_memory)
        self.control_unit = unit.ControlUnit()
        self.hazard_detection_unit = unit.HazardDetectionUnit()
        self.PC_word = 0
        self.pipeline_registers = {
            "IF/ID": pr.PipelineRegister(),
            "ID/EX": pr.PipelineRegister(),
            "EX/MEM": pr.PipelineRegister(),
            "MEM/WB": pr.PipelineRegister(),
        }
        self.forwarding_unit = unit.ForwardingUnit()

    def compile(self):
        self.IF_stage()
        
        # compile the instructions until finished the all instructions 
        
        while(self.PC_word < len(self.memory.get_all_ins_memory())):
           # self.IF_stage()
            #self.ID_stage()
            #WB stage
            #MEM stage
            #EX stage
            #ID stage
            #IF stage
            pass

        return
        

    """you may need some functions to help you to do the pipeline stages, add these to the pipeline register class (def xxxx(): )"""

    def IF_stage(self):
        if self.pipeline_registers['IF/ID'].get_write() ==0:
            return
        print("--------------------------IF stage------------------\n")
        #pc_word

        # print(self.memory.get_ins_memory(self.PC_word)[0])
        split_result = self.memory.get_ins_memory(self.PC_word)[1].split(",")
        if self.memory.get_ins_memory(self.PC_word)[0] == "lw" or self.memory.get_ins_memory(self.PC_word)[0] == "sw":
            if len(split_result) == 2:
                rt = split_result[0].strip()
                temp = split_result[1].split("(")
                immediate = temp[0].strip()
                rs=temp[1].strip(")")
               #check not stall
                if self.pipeline_registers["IF/ID"].get_write() == 1:
                    self.pipeline_registers["IF/ID"].set_registers({"rt": rt, "immediate": immediate, "rs": rs})
                # reg = self.pipeline_registers["IF/ID"].get_register()
                # print(reg)  # {'rt': '$2', 'mem': '8', 'rs': '$0'}

        elif (self.memory.get_ins_memory(self.PC_word)[0] == "add" or self.memory.get_ins_memory(self.PC_word)[0] == "sub"):
            if len(split_result) == 3:
                rd = split_result[0].strip()
                rt = split_result[1].strip()
                rs = split_result[2].strip()
                if self.pipeline_registers["IF/ID"].get_write() == 1:
                    self.pipeline_registers["IF/ID"].set_registers ({"rs": rs,"rt": rt,"rd": rd,})
                # reg=self.pipeline_registers["IF/ID"].get_register()
                # print(reg)  # {'rd': '$6', 'rt': '$4', 'rs': '$5'}
        elif(self.memory.get_ins_memory(self.PC_word)[0]=="beq"):
            if len(split_result) == 3:
                rt = split_result[0].strip()
                rs = split_result[1].strip()
                immediate = split_result[2].strip()
                if self.pipeline_registers["IF/ID"].get_write() == 1:
                    self.pipeline_registers["IF/ID"].set_registers ({"rs": rs,"rt": rt,"immediate": immediate})

        self.pipeline_registers["IF/ID"].set_name(self.memory.get_ins_memory(self.PC_word)[0])
        print(self.pipeline_registers["IF/ID"].get_name())
        print(self.pipeline_registers["IF/ID"].get_register())

        self.PC_word+=1
        self.ID_stage()
       # self.ID_stage()       

        ###self.pipeline_registers['IF/ID'].set_name(self.instruction_memory[self.PC_word][0])
        # fetch the instruction from the instruction memory
        # increment the PC (word) if IF/IDWrite = 1, if IF/IDWrite = 0 then do not fetch the next instruction
        # spilt the instruction into the instruction name and the rest of the line (include registers)
        # add these information to the IF/ID pipeline register (use dict to store the registers and control signals)

        """i used to write this code, may can use it in this stage"""
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
        pass

    def ID_stage(self):
      
        print("---------ID-----------------")
        '''
        print("IF/ID name:" + prp.name + "\n")  # IF/ID 中的指令名稱
        print("IF/ID register:")  # IF/ID 中的register
        print(prp.get_register(prp))'''

        # decide the control signals for the ID/EX pipeline register
        self.control_unit.set_control_signals(self.pipeline_registers["IF/ID"].get_name())
        self.pipeline_registers["ID/EX"].set_control_signals(self.control_unit.get_control_signals())
        print(self.pipeline_registers["ID/EX"].get_control_signals())#{'RegDst': '0', 'ALUSrc': '1', 'Branch': '0', 'MemRead': '1', 'MemWrite': '0', 'RegWrite': '1', 'MemToReg': '1'} 
        

        # read data from the register file, and store the data to the ID/EX pipeline register(if not stall and not forwarding and *branch?*)
        # dazard detection unit
        # forwarding unit
        # check RegDst(use the data self.control_unit.get_control_signals())
        # check forwading here if needed, replace the value of the register with the value in the pipeline register(EX/MEM or MEM/WB)
        '''self.control_unit.set_control_signals(self.pipeline_registers['IF/ID'].name)
         C_S = self.control_unit.get_control_signals()
         self.pipeline_registers['ID/EX'].set_control_signals(C_S)'''

        # check branch (PC adder and reg compare(use the data stored in the pipeline register))
        '''if branch'''
        if(self.pipeline_registers["IF/ID"].get_name()=='beq'):
            rs = self.pipeline_registers['IF/ID'].get_one_register('rs')
            rt = self.pipeline_registers['IF/ID'].get_one_register('rt')
            if(self.register_file.get_register_value(rs) == self.register_file.get_register_value(rt)):
                self.PC_word += self.pipeline_registers['IF/ID'].get_one_register('immediate')
                return
        #IF/ID裡的值(ins,registers)傳給ID/EX   
        self.pipeline_registers["ID/EX"].set_name(self.pipeline_registers["IF/ID"].get_name())
        self.pipeline_registers["ID/EX"].set_registers (self.pipeline_registers["IF/ID"].get_register())
        #print(self.pipeline_registers["ID/EX"].get_name())
        #print(self.pipeline_registers["ID/EX"].get_register())
        self.EX_stage()
        pass

    def EX_stage(self):
        
        print("---------EX-----------------")
        pipeline_register = pr.PipelineRegister()
        if self.pipeline_registers["ID/EX"].IsEmpty():
            return pipeline_register
        
        if self.pipeline_registers["ID/EX"].get_name() == "beq":
            if self.pipeline_registers["EX/MEM"].get_data() == 0:
                self.pipeline_registers["ID/EX"].set_stall()
                self.PC_word = self.PC_word + int(self.pipeline_registers["ID/EX"].get_one_register("immediate"))
            else:
                return pipeline_register
        #check forwarding
        #self.pipeline_registers["EX/MEM"].set_registers ({"rs": '$1',"rt": '$2',"rd":'$4' })#test
        rs = self.pipeline_registers["ID/EX"].get_one_register('rs')
        rs_value=self.register_file.get_register_value(rs)
        rt = self.pipeline_registers["ID/EX"].get_one_register('rt')
        rt_value=self.register_file.get_register_value(rt)

        self.forwarding_unit.set(self.pipeline_registers["ID/EX"], self.pipeline_registers["EX/MEM"], self.pipeline_registers["MEM/WB"],rs_value,rt_value)
        ALUSrc = self.pipeline_registers["ID/EX"].get_one_control_signals('ALUSrc')
        self.forwarding_unit.checkForwarding(ALUSrc)
        
        
        #R-format指令
        #add 
        if(self.pipeline_registers["ID/EX"].get_name()=='add'):
            #運算完結果傳給EX/MEM(data)
            pipeline_register.set_data(self.forwarding_unit.get_rs_value() + self.forwarding_unit.get_rt_value())
        #sub
        elif(self.pipeline_registers["ID/EX"].get_name()=='sub'):   
            pipeline_register.set_data(self.forwarding_unit.get_rt_value() - self.forwarding_unit.get_rs_value())

        #I-format指令
        #從ID/EX讀取指令名稱若為lw或sw則讀取immediate
        if self.pipeline_registers['ID/EX'].get_name()=='lw'|self.pipeline_registers['ID/EX'].get_name()=='sw':
            immediate = self.pipeline_registers["ID/EX"].get_one_register('immediate')
           
        #lw,sw
        elif self.pipeline_registers["ID/EX"].get_name()=='lw'|self.pipeline_registers["ID/EX"].get_name()=='sw':
            
            #offset+rs_value (address=>int((immediate)//4)+self.register_file.get_register_value(rs) ex:w2)
            pipeline_register.set_data('w'+str((int(immediate)//4)+self.forwarding_unit.get_rs_value()))
            
           
        else:
            print("wrong")

        pipeline_register.set_name(self.pipeline_registers["ID/EX"].get_name())
       
        return pipeline_register
        # read data from the register file, and store the data to the EX/MEM pipeline register
        # check ALUSrc
        # calculate the ALU result
        # add the ALU result to the EX/MEM pipeline register

    def MEM_stage(self):
        pass


    def WB_stage(self):
        pass
