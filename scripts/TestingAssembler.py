"""The assembler for the Telescope Assembly Light language"""

# A lot of time is wasted assembling files without an assembler.
# While this project is about doing things from scratch, wasting time is not fun.
# This assembler will be used to write another assembler in the TASL language itself.

# This is also a simulation of the assembler that will be written.
# As a result, there are some odd code style choices that were made throughout this program.
# This was done to make this source code as close to the TASL source code as possible.

# TODO: Combine all tables, separate instruction bitmaps.

import sys

# --------------------------------------Simulation Constants/Globals---------------------------------------
OUTPUT_SUFFIX = ".tlo"
ACCEPTED_IN_SUFFIX = ["tasl", "tl", "rtl"]

LOGISIM_FILE_HEADER = "v2.0 raw"

output_lines = []  # Should be in Logisim's drive format.

input_ROM = []  # Should be characters.
input_pointer = 0  # Would be a physical counter attached to the input_ROM.
output_ROM = []  # Should be 16-bit numbers.

NULL = 0xFFFF

# --------------------------------------Assembler Constants/Globals----------------------------------------
# There will be three tables that the assembler will draw from, in addition to the label table:
# Instruction table entries: (mnemonic_hash, translation, operand_bitmap)
instructions_table = [0xd188, 0x0000, 0b0000,  # HLT
                      0xb672, 0x1000, 0b0000,  # RSM
                      0xcf33, 0x2000, 0b0000,  # SYS
                      0xd9ed, 0x3000, 0b0011,  # MOV
                      0x992a, 0x4000, 0b0100,  # JIF
                      0xa48c, 0x5000, 0b0010,  # LDI
                      0x91ec, 0x6000, 0b0011,  # LOD
                      0xca93, 0x7000, 0b0011,  # STR
                      0xd581, 0x8000, 0b0111,  # ALU
                      0xa581, 0x9000, 0b1111,  # ALI
                      0x9981, 0xA000, 0b0111,  # ALF
                      0x9921, 0xB000, 0b1111,  # AIF
                      0xb981, 0xC000, 0b0111,  # ALN
                      0xb921, 0xD000, 0b1111,  # AIN
                      NULL
                      ]

# Register table entries: (mnemonic_hash, translation)
register_table = [0x40F2, 0x0,  # RG0
                  0x44F2, 0x1,  # RG1
                  0x48F2, 0x2,  # RG2
                  0x4CF2, 0x3,  # RG3
                  0x50F2, 0x4,  # RG4
                  0x54F2, 0x5,  # RG5
                  0x58F2, 0x6,  # RG6
                  0x5CF2, 0x7,  # RG7
                  0x0070, 0x8,  # PC
                  0x01E9, 0x9,  # IO
                  0x9D86, 0xA,  # FLG
                  0x0213, 0xB,  # SP
                  0x8988, 0xC,  # HLB
                  0x9283, 0xD,  # CTD
                  0x8E05, 0xE,  # EPC
                  0x8705, 0xF,  # EXA
                  NULL
                  ]

# Modifier table entries: (mnemonic_hash, translation)
modifier_table = [0xD1EE, 0x0,  # NOT
                  0x91C1, 0x1,  # AND
                  0x024F, 0x2,  # OR
                  0xC9F8, 0x3,  # XOR
                  0x8993, 0x4,  # SLB
                  0x8A53, 0x5,  # SRB
                  0xB0B3, 0x6,  # SEL
                  0x8DC5, 0x7,  # ENC
                  0x9CAE, 0x8,  # NEG
                  0x9081, 0x9,  # ADD
                  0x8C81, 0xA,  # ADC
                  0x8AB3, 0xB,  # SUB
                  0x8853, 0xC,  # SBB
                  0xB2AD, 0xD,  # MUL
                  0xD924, 0xE,  # DIV
                  0x91ED, 0xF,  # MOD

                  0xEA25, 0x0,  # EQZ
                  0xEA8c, 0x1,  # LTZ
                  0xC823, 0x2,  # CAR
                  0xCACF, 0x3,  # OVR
                  0x9250, 0x4,  # PRD
                  0xD2F0, 0x5,  # PWT
                  0xD654, 0x6,  # TRU
                  0x91D2, 0x7,  # RND
                  0xE8AE, 0x8,  # NEZ
                  0xE8A7, 0x9,  # GEZ
                  0xC86E, 0xA,  # NCR
                  0xD9EE, 0xB,  # NOV
                  0xC9D0, 0xC,  # PNR
                  0xDDD0, 0xD,  # PNW
                  NULL
                  ]

# SKIP_CHARS ends in NULL, not because NULL is skipped, but because tables are NULL terminated
SKIP_CHARS = [ord('\n'), ord('\t'), ord('('), ord(')'), ord(' '), ord(','), ord('='), ord(':'), ord('['), ord(']'),
              NULL]

COMMENT_CHAR = ord('/')  # Comments end at a newline character.
NEWLINE_CHAR = ord('\n')
COMMAND_CHAR = ord('%')  # Commands are for later assemblers.
LABEL_CHAR = ord('#')    # Labels end at a skippable character.
CONST_CHAR = ord('@')    # Constants end at a skippable character.
HEX_CHAR = ord('x')      # Hexadecimal numbers can have varying length, and end at a skippable character.
BIN_CHAR = ord('b')      # Binary numbers have the same syntax as hexadecimal numbers.
REF_CHAR = ord('>')      # References replace the following label with the value of the label.
CHAR_CHAR = ord('\'')    # Character syntax works somewhat similar to how it works in python.
#                          However, it forces the assembler to take ANY *single* character and write it to the output.
ARRAY_CHAR = ord('~')    # The number of zeros in the array follows this character, in decimal only.
STOP_CHAR = 0

INPUT_HEAP_SIZE = 64
input_heap = [0] * INPUT_HEAP_SIZE  # The heap that the assembler will use to store words.
input_heap_pointer = 0  # Would be a variable in Logisim.

LABEL_TABLE_HEAP_SIZE = 4096
label_table = [0] * LABEL_TABLE_HEAP_SIZE  # Will contain entries like [size+1,l,a,b,e,l,value,size+1,l,a,...]
#                                            Note: size+1 is the relative index of the value
table_heap_pointer = 0  # Would be a variable in Logisim.


# ------------------------------------------The Simulation--------------------------------------------------
def to_out_format(value):
    """Takes a given value and returns the Logisim formatted version of that number."""

    return hex(value)[2:]


def setup():
    """Makes sure everything is ready for the assembler to run in the simulation."""
    print("Checking the arguments...")

    if len(sys.argv) != 2:
        print("Error: Expected 1 argument (input file path), got " + str(len(sys.argv) - 1) + " instead.")
        exit(2)

    input_file_path = sys.argv[1]
    input_file_suffix = input_file_path.split('.')[1]

    if input_file_suffix != "tasl":
        print("Error: Expected input file type to be in " + str(ACCEPTED_IN_SUFFIX) + ", got a " + input_file_suffix +
              " file instead.")
        exit(2)

    input_file_name = input_file_path.split('.')[0]
    output_file_path = input_file_name + OUTPUT_SUFFIX

    with open(input_file_path, 'r') as in_file:
        print("Done getting arguments, now writing to the simulation ROM input...")
        char = in_file.read(1)
        while char:
            char = ord(char)
            input_ROM.append(char)
            char = in_file.read(1)

    if len(input_ROM) == 0:
        print("Error: input file empty.")
        exit(1)

    input_ROM.append(STOP_CHAR)  # All words after the program until the end of memory would be 0 anyways.
    input_ROM.append(STOP_CHAR)

    print("Starting the assembler...")
    start_point()

    print("Assembler is done running, sending the output ROM contents to the output file...")
    output_lines.append(LOGISIM_FILE_HEADER + "\n")

    for val in output_ROM:
        out = to_out_format(val)
        output_lines.append(out + "\n")

    with open(output_file_path, 'w') as out_file:
        out_file.writelines(output_lines)

    print("The simulation has finished.")


def read_input():
    """
    Returns the next character from the input, incrementing the input pointer.
    This would happen automatically when doing LDI FLG >INPUT_FLG, MOV RG0 IO
    """
    global input_pointer
    next_val = input_ROM[input_pointer]
    input_pointer += 1
    return next_val


def write_0_to_input():
    """Writing 0 to the input circuit resets the pointer."""
    global input_pointer
    input_pointer = 0


def write_output(value):
    """
    Writes the value to the output.
    Would automatically increment some output pointer in Logisim when LDI FLG >OUTPUT_FLG, MOV IO RG0
    """
    output_ROM.append(value)


# -------------------------------------------The Assembler------------------------------------------------
def print_input_heap():  # TODO: Debug only.
    print("Printing heap contents...")
    out = ""
    for i in range(0, input_heap_pointer - 1):
        out = out + chr(input_heap[i]) + " "
    last_elem = input_heap[(input_heap_pointer - 1)]
    out = out + chr(last_elem) + "\n"
    print(out)


def start_point():
    # Reset input
    write_0_to_input()
    # Goto the assembler by calling build_tables.
    build_tables()


def get_value_base(multiplier, starting_index):
    """Assumes the heap currently has some kind of number in it."""
    out = 0
    index = starting_index
    while True:
        if index == input_heap_pointer:
            break

        next_char = input_heap[index]
        if (next_char & 0x40) != 0:  # it's text
            next_char += 9

        next_char = next_char & 0xF
        out = out * multiplier
        out = out + next_char

        index += 1
    return out


def get_numeric_value():
    """Interprets the contents of the input_heap as a number, returns the value."""

    if input_heap_pointer == 1: # it is a 1 digit decimal number
        char = input_heap[0]
        return char & 0xF

    second_char = input_heap[1]

    if (second_char & 0x40) == 0:
        return get_value_base(10, 0)

    elif second_char == HEX_CHAR:
        return get_value_base(16, 2)

    elif second_char == BIN_CHAR:
        return get_value_base(2, 2)

    else:
        print_input_heap()
        print("NUMERIC VALUE TYPE ERROR")
        exit(1)


def label_lookup():
    """Assumes the label to search for is in the heap, like [>,L,a,b,e,l]"""
    table_index = 0

    # Loop through the label table
    while True:
        # Check if we're out of labels to search through.
        if table_index >= table_heap_pointer:
            print("LABEL NOT FOUND ERROR")
            exit(1)

        # Check if the label is the right size.
        size = label_table[table_index]
        if input_heap_pointer == size:
            loop_index = 1

            # Loop through both the input_heap string and the table's string at the same time.
            while True:
                # If we reach the end of the heap, we have a match (cause they're the same size strings).
                if loop_index == input_heap_pointer:
                    return label_table[table_index + size]

                # If any pair of characters don't match, exit the loop.
                if input_heap[loop_index] != label_table[loop_index + table_index]:
                    break

                loop_index += 1

        table_index += size
        table_index += 1


def table_index_lookup(key, table, entry_size):
    """Returns the index of the first entry in the table whose first field matches the key."""
    index = 0
    while True:
        next_entry_key = table[index]

        if next_entry_key == key:
            return index
        if next_entry_key == NULL:
            return NULL

        index += entry_size


def goto_char(target):
    """Reads from the input until it reaches the given character."""
    char = read_input()
    while char != target:
        if char == STOP_CHAR:
            break
        char = read_input()


def get_next_text():
    """Reads the next viable sequence of characters from input into the heap"""

    global input_heap_pointer

    # Look for the start of a viable sequence
    while True:
        char = read_input()
        if char == COMMAND_CHAR:
            goto_char(COMMAND_CHAR)

        elif char == COMMENT_CHAR:
            goto_char(NEWLINE_CHAR)

        else:  # if char is not a skip character
            result = table_index_lookup(char, SKIP_CHARS, 1)
            if result == NULL:
                break  # We've found something that is not skippable.

    # If we hit a stop character, just put that in the input heap.
    if char == STOP_CHAR:
        input_heap[0] = char
        input_heap_pointer = 1
        return

    input_heap_pointer = 0

    # Else, get the rest of the character sequence
    while True:
        input_heap[input_heap_pointer] = char
        input_heap_pointer += 1

        char = read_input()

        if char == COMMAND_CHAR:
            goto_char(COMMAND_CHAR)
            break

        elif char == COMMENT_CHAR:
            goto_char(NEWLINE_CHAR)
            break

        elif char == STOP_CHAR:
            break

        else:  # if char is a skip character
            result = table_index_lookup(char, SKIP_CHARS, 1)
            if result != NULL:
                break

    # Check to see if we tried to read a character that was a skip or character character.
    if input_heap[0] == CHAR_CHAR:

        if input_heap_pointer == 1:
            char = read_input()
            input_heap[1] = char
            input_heap_pointer += 1

        if input_heap_pointer == 2:
            char = read_input()
            input_heap[2] = char
            input_heap_pointer += 1


def append_string_label():
    """Adds the input_heap to the label_table as a label, but does not assign it a value."""
    global table_heap_pointer
    index = 1

    # Add size+1
    label_table[table_heap_pointer] = input_heap_pointer
    table_heap_pointer += 1

    # Copy in the label string
    while index != input_heap_pointer:
        label_table[table_heap_pointer] = input_heap[index]
        table_heap_pointer += 1
        index += 1


def hash_heap():
    """Treats the input_heap as the input for the hash function."""
    out = 0

    temp = input_heap[2] & 0x40
    temp = temp << 9
    out = out | temp

    temp = input_heap[2] & 0x1f
    temp = temp << 10
    out = out | temp

    temp = input_heap[1] & 0x1f
    temp = temp << 5
    out = out | temp

    temp = input_heap[0] & 0x1f
    out = out | temp

    return out


def assemble_next_mnemonic(table):
    """
    Fetches and returns the value of the next mnemonic from the given table.
    CANNOT BE USED FOR INSTRUCTIONS.
    """
    global input_heap_pointer

    get_next_text()

    if input_heap_pointer == 2:
        input_heap[2] = 0
        input_heap_pointer += 1

    hash_val = hash_heap()

    index = table_index_lookup(hash_val, table, 2)

    value_index = index + 1
    value = table[value_index]
    return value


def build_tables():
    """The first pass through the file, we build the tables"""
    global table_heap_pointer

    program_counter = 0
    while True:
        # Place the next chunk of admissible text into the heap.
        get_next_text()
        first_char = input_heap[0]

        # Check what type of admissible string it is.
        if first_char == STOP_CHAR:  # We're done
            break

        elif first_char == LABEL_CHAR:  # It's a label
            # Add the label to the table.
            append_string_label()

            # Add the value to the table.
            label_table[table_heap_pointer] = program_counter
            table_heap_pointer += 1

        elif first_char == CONST_CHAR:  # It's a constant
            # Add the label to the table.
            append_string_label()

            # Get the constant's text value.
            get_next_text()

            # Get and store the value of the label.
            value = get_numeric_value()
            label_table[table_heap_pointer] = value
            table_heap_pointer += 1

        elif first_char == CHAR_CHAR:  # It's a character
            program_counter += 1

        elif first_char == ARRAY_CHAR:  # It's an empty array
            zeros = get_value_base(10, 1)  # A decimal number of zeros follows this character.
            program_counter += zeros

        elif (first_char & 0x40) == 0:  # It's a number
            program_counter += 1

        else:  # It's an instruction
            program_counter += 1

            # Hash the instruction, and lookup how many strings we have to skip.
            hash_key = hash_heap()
            index = table_index_lookup(hash_key, instructions_table, 3)
            bmp_index = index + 2
            bitmap = instructions_table[bmp_index]
            if (bitmap & 0b100) != 0:
                get_next_text()
            if (bitmap & 0b010) != 0:
                get_next_text()
            if (bitmap & 0b001) != 0:
                get_next_text()

    # After we're done, pass control to the actual assembler with the input reset
    write_0_to_input()
    assemble()


def assemble():
    """The second pass through the file, the assembly is translated into machine code."""
    while True:
        # Place the next chunk of admissible text into the heap.
        get_next_text()
        first_char = input_heap[0]

        # Check what type of admissible string it is.
        if first_char != LABEL_CHAR:  # Label declarations are ignored in this pass through.
            if first_char == STOP_CHAR:  # We're done.
                break

            elif first_char == REF_CHAR:  # It is a reference to label.
                value = label_lookup()
                write_output(value)

            elif first_char == CONST_CHAR:  # It is a constant declaration.
                get_next_text()

            elif first_char == CHAR_CHAR:  # It is a character.
                value = input_heap[1]
                write_output(value)

            elif first_char == ARRAY_CHAR:  # It is an empty array, so we make it.
                value = get_value_base(10, 1)
                num_zeros = 0
                while True:
                    if num_zeros == value:
                        break
                    write_output(0)
                    num_zeros += 1

            elif (first_char & 0x40) == 0:  # It is a numeric value.
                value = get_numeric_value()
                write_output(value)

            else:  # It's an instruction.
                # Hash the instruction.
                hash_val = hash_heap()

                # Translate the instruction and get the bitmap.
                index = table_index_lookup(hash_val, instructions_table, 3)
                value_index = index + 1
                out = instructions_table[value_index]
                bmp_index = value_index + 1
                bitmap = instructions_table[bmp_index]

                # Gather operands according to the bitmap.
                if (bitmap & 0b0100) != 0:
                    value = assemble_next_mnemonic(modifier_table)
                    value = value << 8
                    out = out | value

                if (bitmap & 0b0010) != 0:
                    value = assemble_next_mnemonic(register_table)
                    value = value << 4
                    out = out | value

                if (bitmap & 0b0001) != 0:
                    if (bitmap & 0b1000) != 0:
                        get_next_text()
                        value = get_numeric_value()
                        value = value & 0xf
                    else:
                        value = assemble_next_mnemonic(register_table)
                    out = out | value

                write_output(out)


setup()
