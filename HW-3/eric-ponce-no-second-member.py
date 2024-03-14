def main():
  instruction = input("Enter a instruction: \n\n")
  # print(instruction)
  # print(type(instruction))

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
        '001': ['sll'],
        '010': ['slt'],
        '011': ['sltu'],
        '100': ['xor'],
        '101': ['srl', 'sra'],
        '110': ['or'],
        '111': ['and']
    }

    funct7_dict = {
      'add':'0000000',
      'sub':'0100000',
      'srl':'0000000',
      'sra':'0100000'
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

  elif opcode == "0010011":
    # This is an I Type instruction =======================================
    rs1 = instruction[12:17]
    rd = instruction[20:25]
    imm = instruction[0:12]
    imm_decimal = int(imm, 2)
    funct3 = instruction[17:20]

    funct3_dict = {
    '000': ['addi'],
    '001': ['slli'],
    '010': ['slti'],
    '011': ['sltiu'],
    '100': ['xori'],
    '101': ['srai', 'srli'],
    '110': ['ori'],
    '111': ['andi']
    }

    imm_dict = {
      'srli':'0000000',
      'srai':'0100000'
    }

    if funct3 in funct3_dict:
      operations = funct3_dict[funct3]
      if len(operations) == 1:
          operation = operations[0]
      else:
          # Multiple operations, compare to imm
          # print(operations)
          for op in operations:
            if imm_dict[op] == imm[0:7]:
              operation = op

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

    # If the most significant bit is 1, this is a negative number
    if imm[0] == '1':
      imm_decimal -= 2 ** len(imm)

    print("\nInstruction Type: I")
    print("Operation: jalr")
    print(f"Rs1: x{int(rs1, 2)}")
    print(f"Rd: x{int(rd, 2)}")
    print(f"Immediate: {imm_decimal} (or 0x{format(int(imm, 2), 'X')})")

  elif opcode == "0000011":
    # This is the lb, lh, or lw instruction =======================================
    rs1 = instruction[12:17]
    rd = instruction[20:25]
    imm = instruction[0:12]
    imm_decimal = int(imm, 2)
    funct3 = instruction[17:20]

    funct3_dict = {
      '000': 'lb',
      '001': 'lh',
      '010': 'lw',
    }
    
    if funct3 in funct3_dict:
      operation = funct3_dict[funct3]

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
      '000':'sb',
      '001':'sh',
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
      '000':'beq',
      '001':'bne',
      '100':'blt',
      '101':'bge'
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
    
    




if __name__ == "__main__":
  main()