# Global Variables
pc = 0
next_pc = 0

opcode = '0'
rd = '0'
rs1 = '0'
rs2 = '0'
funct3 = '0'
funct7 = '0'
imm = '0'
sign_extended_imm = '0'

register1_val = 0
register2_val = 0

RegWrite = 0
Branch = 0
ALUSrc = 0
ALUOp = 0
MemWrite = 0
MemtoReg = 0
MemRead = 0

alu_ctrl = '0'

rf = ['0'] * 32
rf[1] = '0x20'
rf[2] = '0x5'
rf[10] = '0x70'
rf[11] = '0x4'

# rf[12] = '0x5' # Testing
# rf[13] = '0x1'

alu_zero = 0

d_mem = ['0'] * 32
d_mem[28] = '0x5' # Address: 0x70
d_mem[29] = '0x10' # Address: 0x74

branch_target = 0

total_clock_cycles = 0

new_address = '0'

start_index = 0



# Fetch Function =================================================================================================================================================================
def fetch():
  global pc, next_pc, total_clock_cycles, start_index, branch_target
  userInput = input("Enter the program file name to run: \n\n")
  print('')
  with open(f"Project/{userInput}", "r") as file:
      instruction_set = [line.strip() for line in file.readlines()]

  i = start_index
  while i < len(instruction_set):
      instruction = instruction_set[i]
      pc = (i + 1) * 4
      next_pc = pc + 4
      decode(instruction)
      if branch_target != 0:
          start_index = i + branch_target
          i = start_index  # Reset i to the start index
          branch_target = 0
          continue  # Restart the loop from the new start index
      i += 1

  print("program terminated:")
  print("total execution time is", total_clock_cycles, "cycles")



# Decode Function =================================================================================================================================================================
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



    # print("\nInstruction Type: R")
    # print(f"Operation: {operation}")
    # print(f"Rs1: x{int(rs1, 2)}")
    # print(f"Rs2: x{int(rs2, 2)}")
    # print(f"Rd: x{int(rd, 2)}")
    # print(f"Funct3: {int(funct3, 2)}")
    # print(f"Funct7: {int(funct7, 2)}")

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
    
    # print("\nInstruction Type: I")
    # print(f"Operation: {operation}")
    # print(f"Rs1: x{int(rs1, 2)}")
    # print(f"Rd: x{int(rd, 2)}")
    # print(f"Immediate: {imm_decimal} (or 0x{format(int(imm, 2), 'X')})")
      
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

    # print("\nInstruction Type: I")
    # print("Operation: jalr")
    # print(f"Rs1: x{int(rs1, 2)}")
    # print(f"Rd: x{int(rd, 2)}")
    # print(f"Immediate: {imm_decimal} (or 0x{format(int(imm, 2), 'X')})")

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
    
    # print("\nInstruction Type: I ")
    # print(f"Operation: {operation}")
    # print(f"Rs1: x{int(rs1, 2)}")
    # print(f"Rd: x{int(rd, 2)}")
    # print(f"Immediate: {imm_decimal} (or 0x{format(int(imm, 2), 'X')})")
      
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

    # print("\nInstruction Type: S")
    # print(f"Operation: {operation}")
    # print(f"Rs1: x{int(rs1, 2)}")
    # print(f"Rs2: x{int(rs2, 2)}")
    # print(f"Immediate: {imm_decimal} (or 0x{format(int(imm, 2), 'X')})")
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
  

    # print("Instruction Type: SB \n")
    # print(f"Operation: {operation}")
    # print(f"Rs1: x{int(rs1, 2)}")
    # print(f"Rs2: x{int(rs2, 2)}")
    # print(f"Immediate: {imm_decimal}")
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

    # print("\nInstruction Type: UJ")
    # print("Operation: jal")
    # print(f"Rd: x{int(rd, 2)}")
    # print(f"Immediate: {imm_decimal} (or 0x{format(int(imm, 2), 'X')})")

# Execute Function =================================================================================================================================================================
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
        temp = sign_extended_imm * 2 # Shift sign extended immediate left by 1 (multiply by 2)
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
def Mem():
  global RegWrite, d_mem, rf, new_address

  if RegWrite == 1: #lw
    value = d_mem[int((int(new_address, 16) / 4))]  # Accessing new memory location and retrieving value
    Writeback(value)
  elif RegWrite == 0: #sw
    value = rf[int(rs2, 2)]
    Writeback(value)


# Writeback Function =================================================================================================================================================================
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