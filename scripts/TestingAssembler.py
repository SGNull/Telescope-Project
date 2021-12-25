"""The assembler for the Telescope Assembly Light language"""

# A lot of time is wasted assembling files without an assembler.
# While this project is about doing things from scratch, wasting time is not fun.
# This assembler will be used to write another assembler in the TASL language itself.

# This is also a simulation of the assembler that will be written.
# As a result, there are some odd code style choices that were made throughout this program.
# This was done to make this source code as close to the TASL source code as possible.

# TODO: Add is_hexadecimal() function (455, is first character a number and second a number (or non-existent))
# TODO: Add is_decimal() function (0x23, is first character 0 and second 'x')
# TODO: Add is_binary() function (0b10010101101, is first character 0 and second 'b')
# TODO: Add is_numeric() function (is first character a number)
# TODO: Add get_bin_value() function
# TODO: Add get_numeric() function (all-encompassing function for words being numbers)
# TODO: Add is_array() function ("arr" is in the heap)

import sys

# --------------------------------------Simulation Constants/Globals---------------------------------------
OUTPUT_SUFFIX = ".tlo"
ACCEPTED_IN_SUFFIX = ["tasl", "tl", "rtl"]

LOGISIM_FILE_HEADER = "v2.0 raw"

output_lines = [] # Should be in Logisim's drive format.

input_ROM = [] # Should be characters.
input_pointer = 0 # Would be a physical counter attached to the input_ROM.
output_ROM = [] # Should be 16-bit numbers.

NULL = 0xFFFF

# --------------------------------------Assembler Constants/Globals----------------------------------------
# There will be three tables that the assembler will draw from, in addition to the label table:
# Instruction table entries: (mnemonic_hash, translation, operand_bitmap)
instructions_table = [0xd188, 0x0, 0b000, # HLT
                      0xb672, 0x1, 0b000, # RSM
                      0xcf33, 0x2, 0b000, # SYS
                      0xd9ed, 0x3, 0b011, # MOV
                      0x992a, 0x4, 0b100, # JIF
                      0xa48c, 0x5, 0b010, # LDI
                      0x91ec, 0x6, 0b011, # LOD
                      0xca93, 0x7, 0b011, # STR
                      0xd581, 0x8, 0b111, # ALU
                      0xa581, 0x9, 0b111, # ALI
                      0x9981, 0xA, 0b111, # ALF
                      0x9921, 0xB, 0b111, # AIF
                      0xb981, 0xC, 0b111, # ALN
                      0xb921, 0xD, 0b111, # AIN
                      NULL
                      ]

# Register table entries: (mnemonic_hash, translation)
register_table = [0x40F2, 0x0, # RG0
                  0x44F2, 0x1, # RG1
                  0x48F2, 0x2, # RG2
                  0x4CF2, 0x3, # RG3
                  0x50F2, 0x4, # RG4
                  0x54F2, 0x5, # RG5
                  0x58F2, 0x6, # RG6
                  0x5CF2, 0x7, # RG7
                  0x0070, 0x8, # PC
                  0x01E9, 0x9, # IO
                  0x9D86, 0xA, # FLG
                  0x0213, 0xB, # SP
                  0x8988, 0xC, # HLB
                  0x9283, 0xD, # CTD
                  0x8E05, 0xE, # EPC
                  0x8705, 0xF, # EXA
                  NULL
                  ]

# Modifier table entries: (mnemonic_hash, translation)
modifier_table = [0xD1EE, 0x0, # NOT
                  0x91C1, 0x1, # AND
                  0x024F, 0x2, # OR
                  0xC9F8, 0x3, # XOR
                  0x8993, 0x4, # SLB
                  0x8A53, 0x5, # SRB
                  0xB0B3, 0x6, # SEL
                  0x8DC5, 0x7, # ENC
                  0x9CAE, 0x8, # NEG
                  0x9081, 0x9, # ADD
                  0x8C81, 0xA, # ADC
                  0x8AB3, 0xB, # SUB
                  0x8853, 0xC, # SBB
                  0xB2AD, 0xD, # MUL
                  0xD924, 0xE, # DIV
                  0x91ED, 0xF, # MOD

                  0xEA25, 0x0, # EQZ
                  0xEA8c, 0x1, # LTZ
                  0xC823, 0x2, # CAR
                  0xCACF, 0x3, # OVR
                  0x9250, 0x4, # PRD
                  0xD2F0, 0x5, # PWT
                  0xD654, 0x6, # TRU
                  0x91D2, 0x7, # RND
                  0xE8AE, 0x8, # NEZ
                  0xE8A7, 0x9, # GEZ
                  0xC86E, 0xA, # NCR
                  0xD9EE, 0xB, # NOV
                  0xC9D0, 0xC, # PNR
                  0xDDD0, 0xD, # PNW
                  NULL
                  ]

# SKIP_CHARS ends in NULL, not because NULL is skipped, but because tables are NULL terminated
SKIP_CHARS = [ord('\n'), ord('\t'), ord('('), ord(')'), ord(' '), ord(','), ord('='), ord(':'), ord('['), ord(']'),
              NULL]

TRUE = 1
FALSE = 0

COMMENT_CHAR = ord('/')  # Comments end at a newline character.
NEWLINE_CHAR = ord('\n')
COMMAND_CHAR = ord('%')  # Commands are for later assemblers.
LABEL_CHAR = ord('#')    # Labels end at a skipable character.
CONST_CHAR = ord('@')    # Constants end at a skipable character.
HEX_CHAR = ord('h')      # Hexadecimal numbers can have varying length, and end at a skipable character.
DEC_CHAR = ord('d')      # Decimal numbers have the same syntax as hex numbers.
REF_CHAR = ord('>')      # References replace the following label with the value of the label.
STOP_CHAR = 0

BOT_5_BITS_MASK = 0x1F

INPUT_HEAP_SIZE = 64
input_heap = [0] * INPUT_HEAP_SIZE # The heap that the assembler will use to store words.
input_heap_pointer = 0 # Would be a variable in Logisim.

LABEL_TABLE_HEAP_SIZE = 4096
label_table = [0] * LABEL_TABLE_HEAP_SIZE # Will contain entries like [size+1,l,a,b,e,l,value,size+1,l,a,...]
#                                           Note: size+1 is the relative index of the value
table_heap_pointer = 0 # Would be a variable in Logisim.


# ------------------------------------------The Simulation--------------------------------------------------
def to_out_format(value):
    """Takes a given value and returns the Logisim formatted version of that number."""

    return hex(value)[2:]


def setup():
    """Makes sure everything is ready for the assembler to run in the simulation."""

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
        char = in_file.read(1)
        while char:
            input_ROM.append(char)
            char = in_file.read(1)

    if len(input_ROM) == 0:
        print("Error: input file empty.")
        exit(1)

    input_ROM.append(STOP_CHAR)
    input_ROM.append(STOP_CHAR)

    start_point()

    for val in output_ROM:
        out = to_out_format(val)
        output_lines.append(out + "\n")

    with open(output_file_path, 'w') as out_file:
        out_file.writelines(output_lines)


def read_input():
    """
    Returns the next character from the input, incrementing the input pointer.
    This would happen automatically when doing LDI FLG >INPUT_FLG, MOV RG0 IO
    """
    global input_pointer
    next_val = ord(input_ROM[input_pointer])
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
def start_point():
    # Reset input
    write_0_to_input()
    # Goto the assembler by calling build_tables.
    build_tables()


def get_hex_value():
    """Assumes the heap currently has a hexadecimal number in it."""
    out = 0
    index = 1
    while True:
        if index == input_heap_pointer:
            break
        next_char = input_heap[index]
        if (next_char & 0x40) != 0: # it's text
            next_char += 9
        value = next_char & 0xF
        out = out << 4
        out = out | value
    return out


def get_dec_value():
    """Assumes the heap currently has a decimal number in it."""
    out = 0
    index = 1
    while True:
        if index == input_heap_pointer:
            break
        next_char = input_heap[index]
        temp = next_char & 0xF
        out = out * 10
        out = out + temp
    return out


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
            input_heap_index = 1
            loop_table_index = table_index + 1

            # Loop through both the input_heap string and the table's string at the same time.
            while True:
                # If we reach the end of the heap, we have a match (cause they're the same size strings).
                if input_heap_index == input_heap_pointer:
                    return label_table[table_index + size]

                # If any pair of characters don't match, exit the loop.
                if input_heap[input_heap_index] != label_table[loop_table_index]:
                    break

                input_heap_index += 1
                loop_table_index += 1

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
        char = read_input()
        if char == STOP_CHAR:
            break


def get_next_text():
    """Reads the next viable sequence of characters from input into the heap"""

    global input_heap_pointer
    input_heap_pointer = 0

    # Look for the start of a viable sequence
    while True:
        char = read_input()
        if char == COMMAND_CHAR:
            goto_char(COMMAND_CHAR)
        elif char == COMMENT_CHAR:
            goto_char(NEWLINE_CHAR)
        else: # if char is not a skip character
            result = table_index_lookup(char, SKIP_CHARS, 1)
            if result == NULL:
                break # We've found something that is not skipable.

    # If we hit a stop character, just put that in the input heap.
    if char == STOP_CHAR:
        input_heap[0] = char
        input_heap_pointer = 1
        return

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
        else: # if char is a skip character
            result = table_index_lookup(char, SKIP_CHARS, 1)
            if result != NULL:
                break


def append_string_label():
    """Adds the input_heap to the label_table as a label, but does not assign it a value."""
    global table_heap_pointer
    index = 1

    # Add size+1
    label_table[table_heap_pointer] = input_heap_pointer
    table_heap_pointer += 1

    # Copy in the label string
    while True:
        if index == input_heap_pointer:
            break
        label_table[table_heap_pointer] = input_heap[index]
        table_heap_pointer += 1
        index += 1


def make_label(value):
    """Adds a label to the label table with the given value."""
    global table_heap_pointer

    # Add the label to the table.
    append_string_label()

    # Add the value to the table.
    label_table[table_heap_pointer] = value
    table_heap_pointer += 1


def make_const():
    """Adds a constant to the label table."""
    global table_heap_pointer

    # Add the label to the table.
    append_string_label()

    # Get the constant's text value.
    get_next_text()

    # Check what format it is in, and get the actual value.
    first_char = input_heap[0]
    value = 0
    if first_char == HEX_CHAR:
        value = get_hex_value()
    elif first_char == DEC_CHAR:
        value = get_dec_value()
    else: # Incorrect constant declaration
        print("CONSTANT DECLARATION ERROR")
        exit(1)

    # Store the value
    label_table[table_heap_pointer] = value
    table_heap_pointer += 1


def hash_heap():
    """Treats the input_heap as the input for the hash function."""
    out = 0

    temp = input_heap[2] & 0x40
    temp = temp << 9
    out = out | temp
    temp = input_heap[2] & BOT_5_BITS_MASK
    temp = temp << 10
    out = out | temp
    temp = input_heap[1] & BOT_5_BITS_MASK
    temp = temp << 5
    out = out | temp
    temp = input_heap[0] & BOT_5_BITS_MASK
    out = out | temp

    return out


def build_tables():
    """The first pass through the file, we build the tables"""
    program_counter = 0
    while True:
        # Place the next chunk of admissible text into the heap.
        get_next_text()
        first_char = input_heap[0]

        if first_char == STOP_CHAR: # we're done
            break

        elif first_char == LABEL_CHAR:
            make_label(program_counter)

        elif first_char == CONST_CHAR:
            make_const()

        elif first_char == HEX_CHAR:
            program_counter += 1

        elif first_char == DEC_CHAR:
            program_counter += 1

        elif first_char == REF_CHAR:
            program_counter += 1

        else: # it's an instruction
            program_counter += 1
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
    while True:
        get_next_text()
        first_char = input_heap[0]

        if first_char == STOP_CHAR: # we're done
            break

        elif first_char == HEX_CHAR:
            value = get_hex_value()
            write_output(value)

        elif first_char == DEC_CHAR:
            value = get_dec_value()
            write_output(value)

        elif first_char == REF_CHAR:
            value = label_lookup()
            write_output(value)

        elif (first_char != LABEL_CHAR) and (first_char != CONST_CHAR):
            hash_val = hash_heap()

            index = table_index_lookup(hash_val, instructions_table, 3)
            value_index = index + 1
            value = instructions_table[value_index]
            bmp_index = value_index + 1
            bitmap = instructions_table[bmp_index]

            out = value << 12

            if (bitmap & 0b100) != 0:
                get_next_text()
                hash_val = hash_heap()
                index = table_index_lookup(hash_val, modifier_table, 2)
                value_index = index + 1
                value = modifier_table[value_index]
                value = value << 8
                out = out | value

            if (bitmap & 0b010) != 0:
                get_next_text()
                hash_val = hash_heap()
                index = table_index_lookup(hash_val, register_table, 2)
                value_index = index + 1
                value = register_table[value_index]
                value = value << 4
                out = out | value

            if (bitmap & 0b001) != 0:
                get_next_text()
                hash_val = hash_heap()
                index = table_index_lookup(hash_val, register_table, 2)
                value_index = index + 1
                value = register_table[value_index]
                out = out | value

            write_output(out)


setup()
