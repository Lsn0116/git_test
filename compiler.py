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
        self.forwarding_unit = unit.ForwardingUnit()
        self.pipeline_registers = {
            "IF/ID": pr.PipelineRegister(),
            "ID/EX": pr.PipelineRegister(),
            "EX/MEM": pr.PipelineRegister(),
            "MEM/WB": pr.PipelineRegister(),
        }
        

    def compile(self):
        print("compile\n")
        self.IF_stage()

        # compile the instructions until finished the all instructions
        """
        while(self.PC_word < len(self.memory.get_instruction_memory())):
            #WB stage
            #MEM stage
            #EX stage
            #ID stage
            #IF stage
            pass

        return
        """

    """you may need some functions to help you to do the pipeline stages, add these to the pipeline register class (def xxxx(): )"""

    def IF_stage(self):

        print("--------------------------IF stage------------------\n")
        
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
        self.pipeline_registers["IF/ID"].set_name(self.memory.get_ins_memory(self.PC_word)[0])
        print(self.pipeline_registers["IF/ID"].get_name())
        print(self.pipeline_registers["IF/ID"].get_register())
       

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

         #刪除control signal
        drop_controlSignal = ['MemRead', 'MemWrite', 'RegWrite', 'MemToReg']
        self.pipeline_registers['IF/ID'].remove_control_signals(drop_controlSignal)
        
        pass

    def ID_stage(self, prp):
        print("IF/ID name:" + prp.name + "\n")  # IF/ID 中的指令名稱
        print("IF/ID register:")  # IF/ID 中的register
        print(prp.get_register(prp))

        #  print("\nIF/ID write"+self.write)
        # decide the control signals for the ID/EX pipeline register
        # read data from the register file, and store the data to the ID/EX pipeline register(if not stall and not forwarding and *branch?*)
        # dazard detection unit
        # forwarding unit
        # check RegDst(use the data self.control_unit.get_control_signals())
        # check forwading here if needed, replace the value of the register with the value in the pipeline register(EX/MEM or MEM/WB)
        # self.control_unit.set_control_signals(self.pipeline_registers['IF/ID'].name)
        # C_S = self.control_unit.get_control_signals()
        # self.pipeline_registers['ID/EX'].set_control_signals(C_S)
        # check branch (PC adder and reg compare(use the data stored in the pipeline register))
        rs = self.pipeline_registers['IF/ID'].get_one_register('rs')
        rt = self.pipeline_registers['IF/ID'].get_one_register('rt')
        if(self.register_file.get_register_value(rs) == self.register_file.get_register_value(rt)):
            self.PC_word += self.pipeline_registers['IF/ID'].get_one_register('immediate')
            return
         #刪除control signal
        drop_controlSignal = ['MemRead', 'MemWrite', 'MemToReg']
        self.pipeline_registers['ID/EX'].remove_control_signals(drop_controlSignal)
        
        pass

    def EX_stage(self):
        # check ALUSrc
        # calculate the ALU result
        # add the ALU result to the EX/MEM pipeline register
         #刪除control signal
        drop_controlSignal = ['MemRead', 'MemWrite', 'RegWrite', 'MemToReg']
        self.pipeline_registers['EX/MEM'].remove_control_signals(drop_controlSignal)
        
        pass

    def MEM_stage(self):
        #decide to do load or store
        if self.pipeline_registers['EX/MEM'].get_write() == 1:
            memRead = self.pipeline_registers['EX/MEM'].get_control_signals().get('MemRead')
            memWrite = self.pipeline_registers['EX/MEM'].get_control_signals().get('MemWrite')
            aluResult = self.pipeline_registers['EX/MEM'].get_data() #not this, it would be 'w1' or something like this

            if memRead: #load
                read_address = aluResult
                self.pipeline_registers['MEM/WB'].set_data(self.memory.get_data_memory(read_address))
                #in WB stage, write the data to the register file

            if memWrite: #store
                write_address = aluResult
                rt = self.pipeline_registers['EX/MEM'].get_one_register('rt')
                write_data = self.register_file.get_register_value(rt)
                self.memory.set_data_memory(write_address, write_data)

        #刪除control signal
        drop_controlSignal = ['MemToReg']
        self.pipeline_registers['MEM/WB'].remove_control_signals(drop_controlSignal)
            

    def WB_stage(self):
        ###TODO:
            #check MemToReg -- if 1 then write the data from the memory to the register file, if 0 then write the data from the ALU to the register file
            #but we just write the data to the register file in MEM stage cause in MEM stage we already replace the data
        
        #check pipleline register MEM/WB can write or not
        if self.pipeline_registers['MEM/WB'].write:
            #get the data from the pipeline register that already calculated
            data_to_write = self.pipeline_registers['MEM/WB'].get_data()
            if data_to_write is not None and self.pipeline_registers['MEM/WB'].control_signals.get('RegWrite'):
                destination_register = self.pipeline_registers['MEM/WB'].registers.get('DestinationRegister')
                self.register_file.set_register_value(destination_register, data_to_write)

        #刪除control signal
        drop_controlSignal = []
        self.pipeline_registers['WB'].remove_control_signals(drop_controlSignal)
        
                

    def test_MEM_stage(self):
            
            self.pipeline_registers['EX/MEM'].data['ALUResult'] = 42 
            self.pipeline_registers['EX/MEM'].registers['DestinationRegister'] = '$t0' 
            self.pipeline_registers['EX/MEM'].registers['rt_value'] = 10  
            self.MEM_stage()

            print("After MEM stage:")
            print("Memory Write Address:", self.pipeline_registers['MEM/WB'].data.get('WriteAddress'))
            print("Memory Write Data:", self.pipeline_registers['MEM/WB'].data.get('WriteData'))
            print("Destination Register:", self.pipeline_registers['MEM/WB'].registers.get('DestinationRegister'))
    