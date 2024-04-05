# Global Variables
pc = 0 # This is the program counter which keeps track of the current instruction
next_pc = 0 # This is the next program counter which tracks the next instruction

opcode = '0' # Stores the opcode of an instruction
rd = '0' # Stores the destination register of an instruction
rs1 = '0' # Stores the first register of an instruction
rs2 = '0' # Stores the second register of an instruction
funct3 = '0' # Stores the funct3 of an instruction
funct7 = '0' # Stores the funct7 of an instruction
imm = '0' # Stores the immediate value of an instruction
sign_extended_imm = '0' # Stores the sign extended immediate of a function

register1_val = 0 # Stores the value that the first register holds  
register2_val = 0 # Stores the value that the second register holds

RegWrite = 0 # Stores the RegWrite control unit value
Branch = 0 # Stores the Branch control unit value
ALUSrc = 0 # Stores the ALUSrc control unit value 
ALUOp = 0 # Stores the ALUOp control unit value
MemWrite = 0 # Stores the MemWrite control unit value
MemtoReg = 0 # Stores the MemtoReg control unit value
MemRead = 0 # Stores the MemRead control unit value

alu_ctrl = '0' # Stores the aluctrl value

rf = ['0'] * 32 # Declares an array of size 32 with each entry initialized to 0 by default
rf[1] = '0x20' # Stores 0x20 in position 1 of the register file array
rf[2] = '0x5' # Stores 0x5 in position 2 of the register file array
rf[10] = '0x70' # Stores 0x70 in position 10 of the register file array
rf[11] = '0x4' # Stores 0x4 in position 11 of the register file array

# rf[12] = '0x5' # Testing
# rf[13] = '0x1'

alu_zero = 0 # Stores the value of alu zero

d_mem = ['0'] * 32 # Declares an array of size 32 with each entry initialized to 0 by default
d_mem[28] = '0x5' # Address: 0x70 # Storing 0x5 in position 28 of the data memory array
d_mem[29] = '0x10' # Address: 0x74 # Storing 0x10 in position 29 of the data memory array


branch_target = 0 # Stores the value of the branch target

total_clock_cycles = 0 # Stores the value for the number of clock cycles

new_address = '0' # Stores the value of the new address generated when adding the immediate offset to the target address for load and store word



# Fetch Function =================================================================================================================================================================
# This function starts out by asking the user what text file we wish to read from. The user response is stored and used to open the user specified file. The file is read and the instructions in the file are stored in an array. One instruction is read at a time until there are no instructions left. In this function, we keep track of the ‘pc’ and ‘next_pc’ values which are updated before we call the Decode() function. If at any point the ‘branch_target’ value gets updated to be greater than 0, the function knows that we are branching. The variable ‘i’ is updated by adding the array position of the current instruction to the ‘branch_target’. We reset ‘branch_’target’ back to zero and restart the loop which reading the instructions, this time starting at the new position of ‘i’. Once there are no more instructions to be read, the function prints “Program terminated” and the total clock cycle count. 
def fetch():
  global pc, next_pc, total_clock_cycles, branch_target
  userInput = input("Enter the program file name to run: \n\n")
  print('')
  with open(f"Project/{userInput}", "r") as file:
      instruction_set = [line.strip() for line in file.readlines()]

  i = 0
  while i < len(instruction_set):
      instruction = instruction_set[i]
      pc = (i + 1) * 4
      next_pc = pc + 4
      decode(instruction)
      if branch_target != 0:
          i = i + branch_target
          branch_target = 0
          continue  # Restart the loop from the new start index
      i += 1

  print("program terminated:")
  print("total execution time is", total_clock_cycles, "cycles")



# Decode Function =================================================================================================================================================================
# This function is called by the fetch function every time an instruction is read. The purpose of this function is to read the 32 bit binary and convert it to assembly language. Depending on the instruction type, we obtain the opcode, registers, immediate values, and funct3/7 values from the function. Once the instruction is decoded and the program knows what registers to deal with, the values those registers contain are stored in the variables ‘register1_val’ and ‘register2_val’.  This function is also responsible for generating the sign extended immediate values. Once an instruction is fully decoded the program calls the ControlUnit and Execute functions.  
def decode(instruction):
  global rf, opcode, rd, rs1, rs2, funct3, funct7, imm, sign_extended_imm, d_mem, register1_val, register2_val
  # print("Register File:", rf)
  # print("Data Memory:", d_mem)
  

  opcode = instruction[-7:]
  # print("Opcode:", opcode)
  # print(type(opcode))

  if opcode == "0110011":
    # This is an R Type instruction =======================================

    rs1 = instruction[12:17]
    rs2 = instruction[7:12]
    rd = instruction[20:25]
    funct3 = instruction[17:20]
    funct7 = instruction[0:7]

    funct3_dict = {
        '000': ['add', 'sub'],
        '110': ['or'],
        '111': ['and']
    }

    funct7_dict = {
      'add':'0000000',
      'sub':'0100000',
    }

    if funct3 in funct3_dict:
      operations = funct3_dict[funct3]
      if len(operations) == 1:
          operation = operations[0]
      else:
          # Multiple operations, compare to funct7
          # print(operations)
          for op in operations:
            if funct7_dict[op] == funct7:
              # print(funct7_dict[op])
              # print(op)
              operation = op
      
      if operation == 'add':
        register1_val = int(rf[int(rs1, 2)], 16)
        register2_val = int(rf[int(rs2, 2)], 16)
      elif operation == 'sub':
        register1_val = int(rf[int(rs1, 2)], 16)
        register2_val = int(rf[int(rs2, 2)], 16)
      elif operation == 'or':
        register1_val = int(rf[int(rs1, 2)], 16)
        register2_val = int(rf[int(rs2, 2)], 16)
      elif operation == 'and':
        register1_val = int(rf[int(rs1, 2)], 16)
        register2_val = int(rf[int(rs2, 2)], 16)



    print("\nInstruction Type: R")
    print(f"Operation: {operation}")
    print(f"Rs1: x{int(rs1, 2)}")
    print(f"Rs2: x{int(rs2, 2)}")
    print(f"Rd: x{int(rd, 2)}")
    print(f"Funct3: {int(funct3, 2)}")
    print(f"Funct7: {int(funct7, 2)}")

    ControlUnit()
    Execute()

  elif opcode == "0010011":
    # This is an I Type instruction =======================================
    rs1 = instruction[12:17]
    rd = instruction[20:25]
    imm = instruction[0:12]
    imm_decimal = int(imm, 2)
    funct3 = instruction[17:20]

    funct3_dict = {
    '000': 'addi',
    '110': 'ori',
    '111': 'andi'
    }

    if funct3 in funct3_dict:
      operation = funct3_dict[funct3]

    # Sign extension of immediate value 12 bit -> 32 bit
    if imm[0] == '0':
      sign_extended_imm = '0' * 20 + imm
      sign_extended_imm = int(sign_extended_imm, 2)
    else:
      imm_decimal -= 2 ** len(imm) # Negative number
      sign_extended_imm = '1' * 20 + imm # Representaion of sign extension
      sign_extended_imm = imm_decimal
    
    if operation == 'addi':
      register1_val = int(rf[int(rs1, 2)], 16)
    elif operation == 'ori':
      register1_val = int(rf[int(rs1, 2)], 16)
    elif operation == 'andi':
      register1_val = int(rf[int(rs1, 2)], 16)
    
    print("\nInstruction Type: I")
    print(f"Operation: {operation}")
    print(f"Rs1: x{int(rs1, 2)}")
    print(f"Rd: x{int(rd, 2)}")
    print(f"Immediate: {imm_decimal} (or 0x{format(int(imm, 2), 'X')})")
      
    ControlUnit()
    Execute()

  elif opcode == "1100111":
    # This is the jalr instruction =======================================
    rs1 = instruction[12:17]
    rd = instruction[20:25]
    imm = instruction[0:12]
    imm_decimal = int(imm, 2)
    funct3 = instruction[17:20]

    # Sign extension of immediate value 12 bit -> 32 bit
    if imm[0] == '0':
      sign_extended_imm = '0' * 20 + imm
    else:
      sign_extended_imm = '1' * 20 + imm

    # If the most significant bit is 1, this is a negative number
    if imm[0] == '1':
      imm_decimal -= 2 ** len(imm)

    print("\nInstruction Type: I")
    print("Operation: jalr")
    print(f"Rs1: x{int(rs1, 2)}")
    print(f"Rd: x{int(rd, 2)}")
    print(f"Immediate: {imm_decimal} (or 0x{format(int(imm, 2), 'X')})")

  elif opcode == "0000011":
    # This is the lw instruction =======================================
    rs1 = instruction[12:17]
    rd = instruction[20:25]
    imm = instruction[0:12]
    imm_decimal = int(imm, 2)
    funct3 = instruction[17:20]

    funct3_dict = {
      '010': 'lw',
    }
    
    if funct3 in funct3_dict:
      operation = funct3_dict[funct3]

    # Sign extension of immediate value 12 bit -> 32 bit
    if imm[0] == '0':
      sign_extended_imm = '0' * 20 + imm
      sign_extended_imm = int(sign_extended_imm, 2)
    else:
      imm_decimal -= 2 ** len(imm) # Negative number
      sign_extended_imm = '1' * 20 + imm # Representaion of sign extension
      sign_extended_imm = imm_decimal

    register1_val = int(rf[int(rs1, 2)], 16)
    
    print("\nInstruction Type: I ")
    print(f"Operation: {operation}")
    print(f"Rs1: x{int(rs1, 2)}")
    print(f"Rd: x{int(rd, 2)}")
    print(f"Immediate: {imm_decimal} (or 0x{format(int(imm, 2), 'X')})")
      
    ControlUnit()
    Execute()

  elif opcode == "0100011":
    # This is an S Type instruction =======================================
    rs1 = instruction[12:17]
    rs2 = instruction[7:12]
    imm = instruction[0:7] + instruction[20:25] 
    imm_decimal = int(imm, 2)
    funct3 = instruction[17:20]

    funct3_dict = {
      '010':'sw'
    }

    if funct3 in funct3_dict:
      operation = funct3_dict[funct3]
    
    # If the most significant bit is 1, this is a negative immediate
    if imm[0] == '1':
      imm_decimal -= 2 ** len(imm)
      imm = imm_decimal
    else: # Positive immediate
      imm = int(imm, 2)
    
    register1_val = int(rf[int(rs1, 2)], 16)

    print("\nInstruction Type: S")
    print(f"Operation: {operation}")
    print(f"Rs1: x{int(rs1, 2)}")
    print(f"Rs2: x{int(rs2, 2)}")
    print(f"Immediate: {imm_decimal} ")
    ControlUnit()
    Execute()


  elif opcode == "1100011":
    # This is an SB Type instruction =======================================
    rs1 = instruction[12:17]
    rs2 = instruction[7:12]
    imm = instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24] + '0'
    imm_decimal = int(imm, 2)
    funct3 = instruction[17:20]

    funct3_dict = {
      '000':'beq'
    }

    if funct3 in funct3_dict:
      operation = funct3_dict[funct3]

    # Sign extension of immediate value 12 bit -> 32 bit
    if imm[0] == '0':
      sign_extended_imm = '0' * 20 + imm
      sign_extended_imm = int(sign_extended_imm, 2)
    else:
      imm_decimal -= 2 ** len(imm) # Negative number
      sign_extended_imm = '1' * 20 + imm # Representaion of sign extension
      sign_extended_imm = imm_decimal


    register1_val = int(rf[int(rs1, 2)], 16)
    register2_val = int(rf[int(rs2, 2)], 16)
  

    print("Instruction Type: SB \n")
    print(f"Operation: {operation}")
    print(f"Rs1: x{int(rs1, 2)}")
    print(f"Rs2: x{int(rs2, 2)}")
    print(f"Immediate: {imm_decimal}")
    ControlUnit()
    Execute()

  elif opcode == "1101111":
    # This is a UJ Type instruction =======================================
    rd = instruction[20:25]
    imm = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11] + '0'
    imm_decimal = int(imm, 2)

    # If the most significant bit is 1, this is a negative number
    if imm[0] == '1':
      imm_decimal -= 2 ** len(imm)

    print("\nInstruction Type: UJ")
    print("Operation: jal")
    print(f"Rd: x{int(rd, 2)}")
    print(f"Immediate: {imm_decimal} (or 0x{format(int(imm, 2), 'X')})")

# Execute Function =================================================================================================================================================================
# This function is responsible for handling the arithmetic needed for the specified instruction. Based on the ‘alu_ctrl’ value generated by the ControlUnit() function, the program can decide what arithmetic operation needs to take place (add, sub, or, and). For load and store word instruction, the new address is generated by adding the immediate offset to the target address. This new address tells the program where to load a value from or where to store a value. The Mem() function is called after the new address has been determined. For branching if equal, if the register 1 value minus the register 2 value is equal to 0, the program is told to branch. The ‘alu_ zero’ value changes to 1, indicating a branch, the ‘branch_target’ is generated, and the total clock cycles and the value of pc are printed. If the register 1 value minus the register 2 value is not 0, this program knows this is not the branch is not taken. ‘alu_zero’ is set to 0 and the total clock cycles and pc value are printed. The rest of the instructions are different forms of addition, subtraction, and, and or which are stored in a variable called ‘value’. The value is passed as an argument to the Writeback() function. 
def Execute():
  global rf, ALUOp, alu_zero, alu_ctrl, rs1, rs2, rd, sign_extended_imm, branch_target, next_pc, RegWrite, imm, d_mem, total_clock_cycles, new_address, opcode, sign_extended_imm, register1_val, register2_val

  alu_ctrl_dict = {
    '0000' : 'and',
    '0001' : 'or',
    '0010' : 'add',
    '0110' : 'sub'
  }

  if alu_ctrl in alu_ctrl_dict:
    operation = alu_ctrl_dict[alu_ctrl]
    # print(alu_ctrl)
    # print(operation)

  if operation == 'add':
    if ALUOp == 0: 
      if RegWrite == 1: # lw
        new_address = hex(sign_extended_imm + register1_val) # Adding offset to base address
        Mem()
      elif RegWrite == 0: # sw
        new_address = hex(imm + register1_val) # Adding offset to base address
        Mem()
    elif ALUOp == 10: 
      if opcode == '0110011': # add
        value = hex(register1_val + register2_val) # rs1 and rs2 are in binary so convert them to ints to access array locations, read the values at memory location as ints to complete computation and store the result as a hex value back to the register file
        Writeback(value)
      elif opcode == '0010011': # addi
        value = hex(register1_val + sign_extended_imm) # add rs1 and the sign extended immediate value and store in value
        Writeback(value)
  elif operation == 'sub':
    if ALUOp == 1: # beq
      if (register1_val - register2_val == 0):
        alu_zero = 1 # Both registers values are equal, branch
        # temp = sign_extended_imm * 2 # Shift sign extended immediate left by 1 (multiply by 2)
        # branch_target = temp + next_pc # Add left shifted sign extended immediate to next pc value
        branch_target = sign_extended_imm // 4
        total_clock_cycles = total_clock_cycles + 1 #Increment clock cycle count
        print("total_clock_cycles", total_clock_cycles, ":")
        print("pc is modified to", hex(pc), '\n')
      else:
        alu_zero = 0 # Registers have different values, don't branch
        total_clock_cycles = total_clock_cycles + 1 #Increment clock cycle count
        print("total_clock_cycles", total_clock_cycles, ":")
        print("pc is modified to", hex(pc), '\n')
    elif ALUOp == 10: # sub
      value = hex(register1_val - register2_val)
      Writeback(value)
  elif operation == 'or':
    if opcode == '0110011': # or
      value = hex(register1_val | register2_val)
      Writeback(value)
    elif opcode == '0010011': # ori
      value = hex(register1_val | sign_extended_imm)
      Writeback(value)
  elif operation == 'and':
    if opcode == '0110011': # and
      value = hex(register1_val & register2_val)
      Writeback(value)
    elif opcode == '0010011': # andi
      value = hex(register1_val & sign_extended_imm)
      Writeback(value)

# Mem Function =================================================================================================================================================================
# This function is only used for load and store word instructions. The program checks the current value of ‘RegWrite’ to determine which instruction is currently being dealt with. If ‘RegWrite’ is equal to 1, it is a load word instruction and if it is equal to 0, it is a store word instruction. For load word instructions, the new address calculated in the Execute() function is used to access the data memory of that specified address. The value that address contains is stored in a variable called value. That value is passed as an argument to the Writeback() function. For store word instructions, the value of register 2 is stored in a variable called value and passed as an argument to the Writeback() function. 
def Mem():
  global RegWrite, d_mem, rf, new_address

  if RegWrite == 1: #lw
    value = d_mem[int((int(new_address, 16) / 4))]  # Accessing new memory location and retrieving value
    Writeback(value)
  elif RegWrite == 0: #sw
    value = rf[int(rs2, 2)]
    Writeback(value)


# Writeback Function =================================================================================================================================================================
# This function is responsible for storing the computation result back to a destination register. For store word instructions, the value that was passed as an argument is stored at the specified new address in data memory that was calculated in the Execute() function. The total clock cycles, memory location that was modified, and pc value are printed. For every other instruction that calls the Writeback() function, the value that was passed as an argument is stored in the destination register. The total clock cycles, value that the destination register was changed to, and pc value are printed. 
def Writeback(value):
  global rf, rd, total_clock_cycles, pc, opcode, d_mem

  if opcode == '0100011': # sw
    d_mem[int(int(new_address, 16) / 4)] = value  # Store value into data memory
    total_clock_cycles = total_clock_cycles + 1 # Increment clock cycle count
    print("total_clock_cycles", total_clock_cycles, ":")
    print("memory", new_address, "is modified to", value)
    print("pc is modified to", hex(pc), '\n')
  else:
    rf[int(rd, 2)] = value # Store value to specified register
    total_clock_cycles = total_clock_cycles + 1 # Increment clock cycle count
    print("total_clock_cycles", total_clock_cycles, ":")
    print(f"x{int(rd, 2)}, is modified to", value)
    print("pc is modified to", hex(pc), '\n')

    


# ControlUnit Function =================================================================================================================================================================
# The control unit function is responsible for generating control unit signals and alu control values for each instruction. The variables being updated are ‘RegWrite’, ‘Branch’, ‘ALUSrc’, ‘ALUOp’, ‘MemWrite’, ‘MemtoReg’, ‘MemRead’, and ‘alu_ctrl’. The program will use some of these values later on for other functions, so it is important that the values be changed accurately. 
def ControlUnit():
  global RegWrite, Branch, ALUSrc, ALUOp, MemWrite, MemtoReg, MemRead, alu_ctrl, opcode, funct3, funct7

  if opcode == '0000011': # lw Instruction
    RegWrite = 1
    Branch = 0
    ALUSrc = 1
    ALUOp = 0   # 00
    MemWrite = 0
    MemtoReg = 1
    MemRead = 1

    alu_ctrl = '0010'
  elif opcode == '0100011': # sw Instruction
    RegWrite = 0
    Branch = 0
    ALUSrc = 1
    ALUOp = 0   # 00
    MemWrite = 1
    MemtoReg = 0
    MemRead = 0

    alu_ctrl = '0010'
  elif opcode == '1100011': # beq Instruction
    RegWrite = 0
    Branch = 1
    ALUSrc = 0
    ALUOp = 1   # 01
    MemWrite = 0
    MemtoReg = 0
    MemRead = 0 

    alu_ctrl = '0110'
  elif opcode == '0110011': # R Type Instruction
    RegWrite = 1
    Branch = 0
    ALUSrc = 0
    ALUOp = 10
    MemWrite = 0
    MemtoReg = 0
    MemRead = 0 

    if funct3 == '000':
      if funct7 == '0100000': # sub
        alu_ctrl = '0110'
      else: # add
        alu_ctrl = '0010'
    elif funct3 == '111': # AND 
      alu_ctrl = '0000'
    elif funct3 == '110': #OR
      alu_ctrl = '0001'
    
  elif opcode == '0010011': # I Type Instruction 
    RegWrite = 1
    Branch = 0
    ALUSrc = 1
    ALUOp = 10
    MemWrite = 0
    MemtoReg = 0
    MemRead = 0

    if funct3 == '000': # addi
      alu_ctrl = '0010'
    elif funct3 == '110': # ori
      alu_ctrl = '0001'
    elif funct3 == '111': # andi
      alu_ctrl = '0000'


# Runs the Program =================================================================================================================================================================
fetch()