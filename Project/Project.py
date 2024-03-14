# Global Variables
RegWrite = 0
Branch = 0
ALUSrc = 0
ALUOp = 0
MemWrite = 0
MemtoReg = 0
MemRead = 0

alu_ctrl = '0'

# Fetch Function ==================================================
def fetch():
  pc = 0
  next_pc = pc + 4

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


# Decode Function ===============================================
def decode(instruction):
  rf = [0] * 32
  print("Regsiter File:", rf)

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

    ControlUnit(opcode, funct3, funct7)
    print(RegWrite, Branch, ALUSrc)
    Execute(alu_ctrl)

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

    # If the most significant bit is 1, this is a negative number
    if imm[0] == '1':
      imm_decimal -= 2 ** len(imm)

    print("Instruction Type: SB \n")
    print(f"Operation: {operation}")
    print(f"Rs1: x{int(rs1, 2)}")
    print(f"Rs2: x{int(rs2, 2)}")
    print(f"Immediate: {imm_decimal}")

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

# Execute Function =====================================================
def Execute(alu_ctrl):
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

# Mem Function ========================================================
def Mem():
  pass

# Writeback Function ====================================================
def Writeback():
  pass

# ControlUnit Function =====================================================
def ControlUnit(opcode, funct3, funct7):
  global RegWrite, Branch, ALUSrc, ALUOp, MemWrite, MemtoReg, MemRead, alu_ctrl

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

    if funct3 == '000' and funct7 == '0000000': # add
      alu_ctrl = '0010'
    elif funct3 == '000' and funct7 == '0100000': # sub
      alu_ctrl = '0110'
    elif funct3 == '111' and funct7 == '0000000': # AND
      alu_ctrl = '0000'
    elif funct3 == '110' and funct7 == '0000000': #OR
      alu_ctrl = '0001'


# Runs the Program
fetch()