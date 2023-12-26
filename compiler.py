import registers_N_memories as rnm
import pipeline_register as pr
import unit
import reader

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
        self.cycle = 0

    def compile(self):
        
        
        # compile the instructions until finished the all instructions
    
        while self.PC_word <= len(self.memory.get_all_ins_memory()):
            self.cycle += 1
            if self.cycle == 1:
                f = open("result.txt","w")
            else:
                f=open("result.txt","a")
            print("cycle: ", self.cycle)
            f.write("cycle: ")
            f.write(str(self.cycle) + "\n")
            f.close()

            self.WB_stage()
            MW = self.MEM_stage()
            EM = self.EX_stage()
            DE = self.ID_stage()
            FD = self.IF_stage()

            if self.PC_word == len(self.memory.get_all_ins_memory()):
                if MW.IsEmpty() and EM.IsEmpty() and DE.IsEmpty() and FD.IsEmpty():
                    break

            if self.pipeline_registers["IF/ID"].get_write() == 1:
                self.pipeline_registers["IF/ID"] = FD
            if self.pipeline_registers["ID/EX"].get_write() == 1:
                self.pipeline_registers["ID/EX"] = DE
            if self.pipeline_registers["EX/MEM"].get_write() == 1:
                self.pipeline_registers["EX/MEM"] = EM
            if self.pipeline_registers["MEM/WB"].get_write() == 1:
                self.pipeline_registers["MEM/WB"] = MW

            for i in self.pipeline_registers:
                if self.pipeline_registers[i].get_stall() == 1:
                    self.pipeline_registers[i].clear()
                    continue
            f=open("result.txt","a")
            print("--------------------------------------------------")
            f.write("--------------------------------------------------\n")
            f.close()
            
        
        
        f=open("result.txt","a")
        f.write("\nTotal cycles: " + str(self.cycle) + "\n")
        f.close()
        
        self.memory.print_data_memory("result.txt")
        self.register_file.print_register_values("result.txt")
        
        return

    """you may need some functions to help you to do the pipeline stages, add these to the pipeline register class (def xxxx(): )"""

    def IF_stage(self):
        # if self.pipeline_registers["IF/ID"].get_write() == 0:
        #     return
        # pc_word
        pipeline_register = pr.PipelineRegister()
        if self.PC_word >= len(self.memory.get_all_ins_memory()):
            return pipeline_register

        # fetch the instruction reg from the instruction memory
        split_result = self.memory.get_ins_memory(self.PC_word)[1].split(",")
        if (
            self.memory.get_ins_memory(self.PC_word)[0] == "lw"
            or self.memory.get_ins_memory(self.PC_word)[0] == "sw"
        ):
            if len(split_result) == 2:
                rt = split_result[0].strip()
                temp = split_result[1].split("(")
                immediate = temp[0].strip()
                rs = temp[1].strip(")")
                # check not stall
                pipeline_register.set_registers(
                    {"rt": rt, "immediate": immediate, "rs": rs}
                )
                
        elif (
            self.memory.get_ins_memory(self.PC_word)[0] == "add"
            or self.memory.get_ins_memory(self.PC_word)[0] == "sub"
        ):
            if len(split_result) == 3:
                rd = split_result[0].strip()
                rt = split_result[1].strip()
                rs = split_result[2].strip()
            
                pipeline_register.set_registers(
                    {
                        "rs": rs,
                        "rt": rt,
                        "rd": rd,
                    }
                )
        elif self.memory.get_ins_memory(self.PC_word)[0] == "beq":
            if len(split_result) == 3:
                rt = split_result[0].strip()
                rs = split_result[1].strip()
                immediate = split_result[2].strip()
                pipeline_register.set_registers(
                    {"rs": rs, "rt": rt, "immediate": immediate}
                )


        pipeline_register.set_name(self.memory.get_ins_memory(self.PC_word)[0])
        print("IF: " + self.memory.get_ins_memory(self.PC_word)[0])
        f=open("result.txt","a")
        f.write("IF: " + self.memory.get_ins_memory(self.PC_word)[0] + "\n")
        if self.pipeline_registers["IF/ID"].get_write() == 1:    
            self.PC_word += 1
        return pipeline_register

    def ID_stage(self):
        if (not self.pipeline_registers["IF/ID"].IsEmpty() )and self.pipeline_registers["ID/EX"].get_stall() == 0:
            print("ID: " + self.pipeline_registers["IF/ID"].get_name() + ": " + str(self.pipeline_registers["IF/ID"].get_control_signals()))
            f=open("result.txt","a")
            f.write("ID: " + self.pipeline_registers["IF/ID"].get_name() + ": " + str(self.pipeline_registers["IF/ID"].get_control_signals()) + "\n")
            f.close()
        
        self.pipeline_registers["IF/ID"].set_write(1)
        pipeline_register = pr.PipelineRegister()
        if self.pipeline_registers["IF/ID"].IsEmpty():
            return pipeline_register
        if self.pipeline_registers["ID/EX"].get_stall() == 1:
            pipeline_register.set_stall()
        # decide the control signals for the ID/EX pipeline register
        self.control_unit.clear_control_signals()
        self.control_unit.set_control_signals(
            self.pipeline_registers["IF/ID"].get_name()
        )
        pipeline_register.set_control_signals(self.control_unit.get_control_signals())
        if self.pipeline_registers["ID/EX"].get_name() == "lw":
            self.hazard_detection_unit.set_lw_sw(
                self.pipeline_registers["ID/EX"], self.pipeline_registers["IF/ID"]
            )
            if self.hazard_detection_unit.checkHazard_lw_sw():
                self.pipeline_registers["IF/ID"].set_write(0)
                pipeline_register.set_stall()
                return pipeline_register

        """if branch"""
        # need to use forwading unit
        if self.pipeline_registers["IF/ID"].get_name() == "beq":
            self.hazard_detection_unit.set_beq(
                 self.pipeline_registers["IF/ID"],
                self.pipeline_registers["ID/EX"],
                self.pipeline_registers["EX/MEM"],
            )
            stall = self.hazard_detection_unit.checkHazard_beq()
            if stall:
                self.pipeline_registers["IF/ID"].set_write(0)
                pipeline_register.set_stall()
                return pipeline_register
        # check forwarding
            rs = self.pipeline_registers["IF/ID"].get_one_register("rs")
            rt = self.pipeline_registers["IF/ID"].get_one_register("rt")
            rs_value = self.register_file.get_register_value(rs)
            rt_value = self.register_file.get_register_value(rt)
            self.forwarding_unit.clear()
            self.forwarding_unit.set(
                self.pipeline_registers["IF/ID"],
                self.pipeline_registers["EX/MEM"],
                self.pipeline_registers["MEM/WB"],
                rs_value,
                rt_value,
            )
            
            self.forwarding_unit.checkForwarding_branch()
            rs_value = self.forwarding_unit.get_rs_value()
            rt_value = self.forwarding_unit.get_rt_value()
            if rs_value == rt_value:
                pipeline_register.set_data(0)

        # IF/ID裡的值(ins,registers)傳給ID/EX
        pipeline_register.set_name(self.pipeline_registers["IF/ID"].get_name())
        pipeline_register.set_registers(self.pipeline_registers["IF/ID"].get_register())
        return pipeline_register

    def EX_stage(self):
        if not self.pipeline_registers["ID/EX"].IsEmpty():
            print("EX: " + self.pipeline_registers["ID/EX"].get_name() + ": " + str(self.pipeline_registers["ID/EX"].get_control_signals()))
            f=open("result.txt","a")
            f.write("EX: " + self.pipeline_registers["ID/EX"].get_name() + ": " + str(self.pipeline_registers["ID/EX"].get_control_signals())+ "\n")
            f.close()

        
        pipeline_register = pr.PipelineRegister()
        if self.pipeline_registers["ID/EX"].IsEmpty():
            return pipeline_register
        
        if self.pipeline_registers["ID/EX"].get_name() == "beq":
            if self.pipeline_registers["ID/EX"].get_data() == 0:
                self.pipeline_registers["ID/EX"].set_stall()
                self.PC_word = self.PC_word + int(self.pipeline_registers["ID/EX"].get_one_register("immediate"))-1
            else:
                pipeline_register.set_control_signals(self.pipeline_registers["ID/EX"].get_control_signals())
                pipeline_register.set_name(self.pipeline_registers["ID/EX"].get_name())
                pipeline_register.set_registers(self.pipeline_registers["ID/EX"].get_register())
                return pipeline_register
        #check forwarding
        rs = self.pipeline_registers["ID/EX"].get_one_register('rs')
        rs_value=self.register_file.get_register_value(rs)
        rt = self.pipeline_registers["ID/EX"].get_one_register('rt')
        rt_value=self.register_file.get_register_value(rt)

        self.forwarding_unit.set(self.pipeline_registers["ID/EX"], self.pipeline_registers["EX/MEM"], self.pipeline_registers["MEM/WB"],rs_value,rt_value)
        ALUSrc = self.pipeline_registers["ID/EX"].get_one_control_signals('ALUSrc')
        if ALUSrc == '1':
             immediate = self.pipeline_registers["ID/EX"].get_one_register('immediate')
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
        #lw or sw
        if ALUSrc == '1':
            #offset+rs_value (address=>int((immediate)//4)+self.register_file.get_register_value(rs) ex:w2)
            pipeline_register.set_data('w'+str((int(immediate)//4)+self.forwarding_unit.get_rs_value()))

        pipeline_register.set_name(self.pipeline_registers["ID/EX"].get_name())
        pipeline_register.set_registers(self.pipeline_registers["ID/EX"].get_register())
        pipeline_register.set_control_signals(self.pipeline_registers["ID/EX"].get_control_signals())
        pipeline_register.remove_control_signals(['RegDst','ALUSrc'])
        return pipeline_register
        

    def MEM_stage(self):
        if not self.pipeline_registers["EX/MEM"].IsEmpty():
            print("MEM: " + self.pipeline_registers["EX/MEM"].get_name() + ": " + str(self.pipeline_registers["EX/MEM"].get_control_signals()))
            f=open("result.txt","a")
            f.write("MEM: " + self.pipeline_registers["EX/MEM"].get_name() + ": " + str(self.pipeline_registers["EX/MEM"].get_control_signals())+ "\n")
            f.close()
        pipeline_register = pr.PipelineRegister()
        if self.pipeline_registers["EX/MEM"].IsEmpty():
            return pipeline_register
        #decide to do load or store
        if self.pipeline_registers['EX/MEM'].get_write() == 1:
            memRead = self.pipeline_registers['EX/MEM'].get_control_signals().get('MemRead')
            memWrite = self.pipeline_registers['EX/MEM'].get_control_signals().get('MemWrite')
            aluResult = self.pipeline_registers['EX/MEM'].get_data() #not this, it would be 'w1' or something like this
            rt_value = self.register_file.get_register_value(self.pipeline_registers['EX/MEM'].get_one_register('rt'))
            # Forwarding 
            self.forwarding_unit.clear()
            self.forwarding_unit.set_sw(self.pipeline_registers["EX/MEM"], self.pipeline_registers["MEM/WB"],rt_value)
            rt_value = self.forwarding_unit.checkForwarding_sw()
            
            

            if memRead == '1': #load
                read_address = aluResult
                data = self.memory.get_data_memory(read_address)
                pipeline_register.set_data(data)
                pipeline_register.set_name(self.pipeline_registers["EX/MEM"].get_name())
                pipeline_register.set_registers(self.pipeline_registers["EX/MEM"].get_register())
                pipeline_register.set_control_signals(self.pipeline_registers["EX/MEM"].get_control_signals())
                
                #in WB stage, write the data to the register file

            elif memWrite == '1': #store
                write_address = aluResult
                self.memory.set_data_memory(write_address, rt_value)
                pipeline_register.set_data(rt_value)
                pipeline_register.set_name(self.pipeline_registers["EX/MEM"].get_name())
                pipeline_register.set_registers(self.pipeline_registers["EX/MEM"].get_register())
                pipeline_register.set_control_signals(self.pipeline_registers["EX/MEM"].get_control_signals())
            
            else:
                pipeline_register.set_name(self.pipeline_registers["EX/MEM"].get_name())
                pipeline_register.set_registers(self.pipeline_registers["EX/MEM"].get_register())
                pipeline_register.set_control_signals(self.pipeline_registers["EX/MEM"].get_control_signals())
                pipeline_register.set_data(aluResult)

            #刪除control signal
        drop_controlSignal = ['MemRead','MemWrite','Branch']
        pipeline_register.remove_control_signals(drop_controlSignal)
        
        return pipeline_register    


    def WB_stage(self):
        if not self.pipeline_registers["MEM/WB"].IsEmpty():
            print("WB: " + self.pipeline_registers["MEM/WB"].get_name() + ": " + str(self.pipeline_registers["MEM/WB"].get_control_signals()))
            f=open("result.txt","a")
            f.write("WB: " + self.pipeline_registers["MEM/WB"].get_name() + ": " + str(self.pipeline_registers["MEM/WB"].get_control_signals())+ "\n")
            f.close()
        if self.pipeline_registers['MEM/WB'].IsEmpty():
            return
        
        if self.pipeline_registers['MEM/WB'].get_write() == 1:
            data_to_write = self.pipeline_registers['MEM/WB'].get_data()
            mem_to_reg = self.pipeline_registers['MEM/WB'].get_one_control_signals('MemToReg')
            RegWrite = self.pipeline_registers['MEM/WB'].get_one_control_signals('RegWrite')
            Dst=''
            if RegWrite == '1':
                if mem_to_reg == '1':
                    if self.pipeline_registers['MEM/WB'].get_name() == 'lw':
                        Dst = self.pipeline_registers['MEM/WB'].get_one_register('rt')
                        
                elif mem_to_reg != 'X':
                    Dst = self.pipeline_registers['MEM/WB'].get_one_register('rd')   
                if Dst != '':
                    self.register_file.set_register_value(Dst, data_to_write)
                return
    
                

  
    