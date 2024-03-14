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

alu_zero = 0

d_mem = ['0'] * 32
d_mem[28] = '0x5' # Address: 0x70
d_mem[27] = '0x10' # Address: 0x74

branch_target = 0

total_clock_cycles = 0



# Fetch Function =================================================================================================================================================================
def fetch():
  global pc, next_pc

  with open("Project/sample_part1.txt", "r") as file:
    instruction_set = [line.strip() for line in file.readlines()]
    print(instruction_set)  # This is the instructions stored in an array
  
  for instruction in instruction_set:
    pc = pc + 4
    next_pc = pc + 4
    print("Instruction", instruction)
    print("PC:", hex(pc))
    print("Next PC:", hex(next_pc))
    decode(instruction) # Runs the Decode() Function, passing the current instruction as an argument
    print('\n')


# Decode Function =================================================================================================================================================================
def decode(instruction):
  global rf, opcode, rd, rs1, rs2, funct3, funct7, imm, sign_extended_imm
  print("Register File:", rf)
  

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

    print("\nInstruction Type: R")
    print(f"Operation: {operation}")
    print(f"Rs1: x{int(rs1, 2)}")
    print(f"Rs2: x{int(rs2, 2)}")
    print(f"Rd: x{int(rd, 2)}")
    print(f"Funct3: {int(funct3, 2)}")
    print(f"Funct7: {int(funct7, 2)}")

    ControlUnit()
    print(RegWrite, Branch, ALUSrc)
    Execute()

  elif opcode == "0010011":
    # This is an I Type instruction =======================================
    rs1 = instruction[12:17]
    rd = instruction[20:25]
    imm = instruction[0:12]
    imm_decimal = int(imm, 2)
    funct3 = instruction[17:20]

    funct3_dict = {
    '000': ['addi'],
    '110': ['ori'],
    '111': ['andi']
    }

    if funct3 in funct3_dict:
      operations = funct3_dict[funct3]

    # Sign extension of immediate value 12 bit -> 32 bit
    if imm[0] == '0':
      sign_extended_imm = '0' * 20 + imm
    else:
      sign_extended_imm = '1' * 20 + imm

    # If the most significant bit is 1, this is a negative number
    if imm[0] == '1':
      imm_decimal -= 2 ** len(imm)
    
    
    print("\nInstruction Type: I")
    print(f"Operation: {operation}")
    print(f"Rs1: x{int(rs1, 2)}")
    print(f"Rd: x{int(rd, 2)}")
    print(f"Immediate: {imm_decimal} (or 0x{format(int(imm, 2), 'X')})")

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
    else:
      sign_extended_imm = '1' * 20 + imm


    # If the most significant bit is 1, this is a negative number
    if imm[0] == '1':
      imm_decimal -= 2 ** len(imm)
    
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
    
    # If the most significant bit is 1, this is a negative number
    if imm[0] == '1':
      imm_decimal -= 2 ** len(imm)

    print("\nInstruction Type: S")
    print(f"Operation: {operation}")
    print(f"Rs1: x{int(rs1, 2)}")
    print(f"Rs2: x{int(rs2, 2)}")
    print(f"Immediate: {imm_decimal} (or 0x{format(int(imm, 2), 'X')})")


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
    else:
      sign_extended_imm = '1' * 20 + imm

    # If the most significant bit is 1, this is a negative number
    if imm[0] == '1':
      imm_decimal -= 2 ** len(imm)

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
def Execute():
  global rf, ALUOp, alu_zero, alu_ctrl, rs1, rs2, rd, sign_extended_imm, branch_target, next_pc, RegWrite, imm, d_mem

  alu_ctrl_dict = {
    '0000' : 'and',
    '0001' : 'or',
    '0010' : 'add',
    '0110' : 'sub'
  }

  if alu_ctrl in alu_ctrl_dict:
    operation = alu_ctrl_dict[alu_ctrl]
    print(alu_ctrl)
    print(operation)

  # R Type Instructions
  if operation == 'add':
    if ALUOp == 0: 
      if RegWrite == 1: #lw
        print("I AM HERE", rf[int(rs1, 2)])
        temp = hex(int(imm, 2) + int(rf[int(rs1, 2)], 16))
        temp = d_mem[(int(temp, 16) / 4)]
        print(temp)
      elif RegWrite == 0: #0
        pass
    elif ALUOp == 10: # add
      rf[int(rd, 2)] = hex(int(rf[int(rs1, 2)], 16) + int(rf[int(rs2, 2)], 16)) # rs1 and rs2 are in binary so convert them to int to access array locations, read the values at memory location as ints to complete computation and store the result as a hex value back to the register file
      print("TEST ADDITION:", rf[int(rd, 2)])
  elif operation == 'sub':
    if ALUOp == 1: # beq
      if (int(rf[int(rs1, 2)], 16) - int(rf[int(rs2, 2)], 16) == 0):
        alu_zero = 1 # Both registers values are equal, branch
        temp = sign_extended_imm[1:] + '0' # Shift sign extended immediate left by 1
        temp = int(temp, 2) + next_pc # Add left shifted sign extended immediate to next pc value
      else:
        alu_zero = 0 # Registers have different values, don't branch
    elif ALUOp == 10: # sub
      rf[int(rd, 2)] = hex(int(rf[int(rs1, 2)], 16) - int(rf[int(rs2, 2)], 16))
      print("TEST SUBTRATION:", rf[int(rd, 2)])
  elif operation == 'or':
    if ALUOp == 10: # or
      # rf[rd] = rf[rs1] or rf[rs2]
      pass
  elif operation == 'and':
    if ALUOp == 10: # and
      # rf[rd] = rf[rs1] and rf[rs2]
      pass

# Mem Function =================================================================================================================================================================
def Mem():
  pass

# Writeback Function =================================================================================================================================================================
def Writeback():
  pass

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
  elif opcode == '0110011' or opcode == '0010011': # R Type and I Type Instructions
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


# Runs the Program =================================================================================================================================================================
fetch()