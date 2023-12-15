#control the datapath and the pipeline stages
#fetch
#decode (check stalls here if needed)
#execute(check forwading here if needed(EX/MEM.rd =ID/EX.rs or rt))
#memory(check forwarding here if needed(MEM/WB.rd =ID/EX.rs or rt)and not (EX/MEM.rd =ID/EX.rs or rt))
#writeback
#while loop for each cycle (until all instructions are finished)
#check which stage is not empty and move the instruction to the next stage
#if there is no instruction then fetch the first instruction
#each stage would check the pipeline register and control signals to see what to do
#ID stage check stalls 
#check if the instruction is finished and remove it from the pipeline