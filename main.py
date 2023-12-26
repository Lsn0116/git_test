import reader
import compiler
#simulate MIPS pipeline with forwarding and stalling
#read instructions from file
#parse instructions
r = reader.Reader("memory.txt")
ins_memory = r.get_ins_memory() #('instruction', ['rs, rt, rd'] ) ex: ('add', ['$1, $2, $3'])

#simulate pipeline
c=compiler.Compiler(ins_memory)
c.compile()


