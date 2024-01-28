import sys

def parse_line(line):
    fields = line.split()
    label, opcode, operand = '', '', ''
    if len(fields) >= 3:
        label, opcode, operand = fields[:3]
    elif len(fields) >= 1:
        opcode = fields[0]
    return label.upper(), opcode.upper(), operand.upper()

def calculate_locctr_increment(opcode, operand):
    if opcode == 'RESW':
        return 3 * int(operand)
    elif opcode == 'RESB':
        return int(operand)
    elif opcode == 'BYTE':
        if operand.startswith('C'):
            return len(operand) - 3
        elif operand.startswith('X'):
            return (len(operand) - 3) // 2
    elif opcode.startswith('+'):
        return 4
    elif opcode in ['CLEAR', 'COMPR', 'TIXR']:
        return 2
    elif opcode in ['BASE']:
        return 0
    else:
        return 3

def sicxe_assembler_pass1(input_file, output_file, output_file2):
    symtab = {}
    locctr = 0
    starting_address = 0
    program_length = 0

    with open(input_file, 'r') as input_file, open(output_file, 'w') as output_file:
        for line in input_file:
            label, opcode, operand = parse_line(line)
            if opcode == 'START':
                starting_address = int(operand, 16)
                locctr = starting_address
                output_file.write(line)
                continue
            elif opcode == 'END':
                program_length = locctr - starting_address
                output_file.write(line)
                break

            if label and label not in symtab:
                symtab[label] = locctr
            elif label:
                print(f"Error: Duplicate symbol '{label}'")
                continue

            output_file.write(f"{line.rstrip()} {hex(locctr)}\n")
            locctr += calculate_locctr_increment(opcode, operand)

    with open(output_file2, 'w') as symtab_file:
        symtab_file.write("Symbol Table:\n")
        for symbol, address in symtab.items():
            formatted_hex = f"{address:#06X}"
            symtab_file.write(f"{symbol}: {formatted_hex}\n")
            print(f"{symbol}: {formatted_hex}")

    print(f"Program Length: {program_length}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python your_program.py <input_filename> <output_filename> <output_filename_2>")
        sys.exit(1)
    sicxe_assembler_pass1(sys.argv[1], sys.argv[2], sys.argv[3])