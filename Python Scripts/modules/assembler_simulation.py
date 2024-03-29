"""
A simulation of the TASL self-assembler.

What to know:
    - input_ROM: Must be directly set before doing anything.
    - output_ROM: Where the output of the assembler is placed.
    - generate_loadable: If true it generates loadable machine code, else it generates plain machine code.
    - start_point: Run this function to run the assembler on the input.
    - build_tables: Builds the label_table based on the input.
    - assemble: Generates the output data based on the input and the label_table.
"""

# Original Description:
# A lot of time is wasted assembling files without an assembler.
# While this project is about doing things from scratch, wasting time is not fun.
# This assembler was used to write another assembler in the TASL language itself.

# This is also a simulation of an assembler that functions very similar to the self-assembler.
# As a result, there are some odd code style choices that were made throughout this program.
# This was done to make this source code as close to the TASL source code as possible.


# Hardware defined constants:
NULL = 0xFFFF

# Special instruction hashes:
CAL_HASH = 0xb023

# Tables:
# Instruction table entries: (mnemonic_hash, translation, operand_bitmap(1 = operand required) )
instructions_table = [
    0xd188, 0x0000, 0b0000,  # HLT
    0xb672, 0x1000, 0b0000,  # RSM
    0xcf33, 0x2000, 0b0000,  # SYS
    0xd9ed, 0x3000, 0b0011,  # MOV
    0x992a, 0x4000, 0b0100,  # JIF
    0xa48c, 0x5000, 0b0010,  # LDI
    0x91ec, 0x6000, 0b0011,  # LOD
    0xca93, 0x7000, 0b0011,  # STR
    0x9981, 0x8000, 0b0111,  # ALF
    0x9921, 0x9000, 0b1111,  # AIF
    0xd581, 0xA000, 0b0111,  # ALU
    0xa581, 0xB000, 0b1111,  # ALI
    0xb8c1, 0xC000, 0b0111,  # AFN
    0xb921, 0xD000, 0b1111,  # AIN
    0xc1ee, 0xF000, 0b0000,  # NOP

    0xd0b2, 0x3087, 0b0000,  # RET
    0xbe5a, 0xb100, 0b0010,  # ZRO
    0xb2ae, 0xb000, 0b0010,  # NUL
    0xcc30, 0x9200, 0b0010,  # PAS

    0x8dc9, 0xb901, 0b0010,  # INC
    0x8ca4, 0xbb01, 0b0010,  # DEC
    0x8c69, 0x9901, 0b0010,  # ICC (inc +set flags)
    0x8c64, 0x9b01, 0b0010,  # DCC (dec +set flags)
    0xa270, 0xbbb0, 0b1001,  # PSH
    0xc1f0, 0xb9b0, 0b1001,  # POP
    0xc1a3, 0xcb00, 0b0011,  # CMP
    0xa5a3, 0xdb00, 0b1011,  # CMI

    0xc1aa, 0x4600, 0b0000,  # JMP
    0xc4aa, 0x4000, 0b0000,  # JEQ
    0x95ca, 0x4800, 0b0000,  # JNE
    0xd18a, 0x4100, 0b0000,  # JLT
    0x94ea, 0x4900, 0b0000,  # JGE
    NULL
]

# Register table entries: (mnemonic_hash, translation)
register_table = [
    # General purpose:
    0x40F2, 0x0,  # RG0
    0x44F2, 0x1,  # RG1
    0x48F2, 0x2,  # RG2
    0x4CF2, 0x3,  # RG3

    # No longer used:
    0x50F2, 0x4,  # RG4
    0x54F2, 0x5,  # RG5
    0x58F2, 0x6,  # RG6
    0x5CF2, 0x7,  # RG7

    # Assembler assigned special purpose:
    0x40d3, 0x4,  # SF0
    0x44d3, 0x5,  # SF1
    0xD2AF, 0x6,  # OUT
    0x0032, 0x7,  # RA

    # Special purpose:
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
modifier_table = [
    0xD1EE, 0x0,  # NOT
    0x91C1, 0x1,  # AND
    0x024F, 0x2,  # OR
    0xC9F8, 0x3,  # XOR
    0x8993, 0x4,  # SLB
    0x8A53, 0x5,  # SRB
    0xd0b3, 0x6,  # SET
    0xd275, 0x7,  # UST
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


# Special characters:
COMMENT_CHAR = ord('/')     # Comments end at a newline character.
NEWLINE_CHAR = ord('\n')
MULTI_LINE_CHAR = ord('%')  # Multi-line comments start and end with '%'
LABEL_CHAR = ord('#')       # Labels end at a skippable character.
CONST_CHAR = ord('@')       # Constants end at a skippable character.
HEX_CHAR = ord('x')         # Hexadecimal numbers can have varying length, and end at a skippable character.
BIN_CHAR = ord('b')         # Binary numbers have the same syntax as hexadecimal numbers.
REF_CHAR = ord('>')         # References replace the following label with the value of the label.
CHAR_CHAR = ord("'")        # Character syntax works somewhat similar to how it works in python. However,
#                             it forces the assembler to take ANY *single* character and write it to the output.
STRING_CHAR = ord('"')      # Places a series of characters in order in memory, followed by NULL.
ARRAY_CHAR = ord('~')       # The number of zeros in the array follows this character.
NEGATIVE_CHAR = ord('-')
STOP_CHAR = 0


# Memory management:
BUFFER_HEAP_SIZE = 128              # We do not expect anyone to type anything larger than 128 characters.
buffer = [0] * BUFFER_HEAP_SIZE     # The heap that the assembler will use to store words.
buffer_index = 0                    # Would be a variable in Logisim.

LABEL_TABLE_HEAP_SIZE = 0x2000      # Somewhat arbitrary. Need enough space, but not too much.
label_table = [0] * LABEL_TABLE_HEAP_SIZE  # Will contain entries like [size+1,l,a,b,e,l,value,size+1,l,a,...]
#                                            Note: size+1 happens to be the relative index of "value"
label_table_index = 0               # Would be a variable in Logisim.

input_ROM: [int] = []  # Needs to be initialized at some point before running. This is handled externally.
output_ROM: [int] = []
input_pointer = 0


# Assembler options:
generate_loadable = False  # Needs to be global because it effects the assembler.


# =========================================== Simulation Functions ===========================================


def read_input() -> int:
    """
    Returns the next input char, and increments the input pointer.

    This simulates reading from the input ROM at the hardware level.
    """
    global input_pointer
    next_val = input_ROM[input_pointer]
    input_pointer += 1
    return next_val


def write_0_to_input() -> None:
    """Writes 0 to the input circuit, resetting the input pointer."""
    global input_pointer
    input_pointer = 0


def write_output(value: int) -> None:
    """
    Writes the value to the output.

    This would automatically increment some output pointer at the hardware level.
    """
    output_ROM.append(value)


def SEL(value: int, bit: int) -> int:
    """
    Returns bit number 'bit' of 'value'.

    Deprecated in hardware; what was SEL is now the carry output of SET and UST.
    """
    mask = 1 << bit
    return (mask & value) >> bit


def print_buffer() -> None:
    """Prints the contents of the buffer to the console for debugging."""
    print("Printing heap contents...")
    print(buffer_as_string() + "\n")


def buffer_as_string() -> str:
    """Returns the contents of the buffer as a string."""
    buf_string = ""
    for i in range(0, buffer_index):
        buf_string += chr(buffer[i])

    return buf_string


# ========================================== The Assembler ================================================


def start_point() -> None:
    """The first function to run in the assembler."""

    # Build the label table
    build_tables()
    # Call the assembler
    assemble()


def is_char_important(char_num: int) -> bool:
    """Check if a given character is 'important' or not."""

    # First check if it's the stop character
    if char_num == STOP_CHAR:
        return True

    # This check includes uppercase, lowercase, and some other symbols that we may care about
    if char_num > 63:
        mod_char = char_num & ~0b100000

        if mod_char < 91:  # It's a letter
            return True
        if mod_char < 94:  # It's something like {}, [], | or \
            return False

        return True  # It's either ^ ~ or _

    # Check if it's a reference character
    if char_num == REF_CHAR:
        return True

    # Now check if it's a comment char or a number
    elif 58 > char_num > 44:
        return True

    # Finally, check for some special symbols.
    elif 40 > char_num > 32:
        return True

    # If it fell through all checks, return false
    return False


def get_value_base(base_num: int, starting_index: int) -> int:
    """Get the value of the heap beginning at 'starting index' in base 'base_num.' Also checks for negative."""

    # Set up the loop
    out = 0
    index = starting_index
    while True:
        if index == buffer_index:
            break

        # Get the next character and adjust it's value properly.
        next_char = buffer[index]
        if (next_char & 0x40) != 0:  # it's text
            next_char += 9

        # Shift the total by 'base_num' then add the character's value to it.
        out = out * base_num
        next_char = next_char & 0xF
        out = out + next_char

        # Close the loop properly.
        index += 1

    if buffer[0] == NEGATIVE_CHAR:
        out = -out

    return out


def get_numeric_value() -> int:
    """Interprets the contents of the buffer as a number, and returns its value."""
    first_char = buffer[0]

    # This is the "label hack" trick.
    if first_char == REF_CHAR:  # This can, if used incorrectly, cause problems.
        return label_lookup()  # its effects are pretty cool, though. You can do @MY_CONST = >MY_OTHER_CONST
    #                            ...so long as MY_OTHER_CONST is already defined. If not, RIP.

    # If it is a 1 digit decimal number, just return it's value.
    if buffer_index == 1:
        return first_char & 0xF

    # Check if this is a negative number
    is_negative = 0
    if first_char == NEGATIVE_CHAR:
        is_negative = 1
        first_char = buffer[1]

    # Check if this is a 1 digit negative decimal number.
    if buffer_index == 2:
        if is_negative:
            return -(first_char & 0xF)

    # Now check the second character to see which type of number this is.
    second_char = buffer[1 + is_negative]
    if (second_char & 0x40) == 0:  # If the second character is a number, it's decimal.
        return get_value_base(10, 0 + is_negative)

    elif second_char == HEX_CHAR:
        return get_value_base(16, 2 + is_negative)

    elif second_char == BIN_CHAR:
        return get_value_base(2, 2 + is_negative)

    else:
        print_buffer()
        print("NUMERIC VALUE TYPE ERROR")
        raise ValueError


def label_lookup() -> int:
    """Takes the label found in the heap (like [>,L,a,b,l,e]) and returns its value from the label table."""
    table_index = 0

    # Loop through the label table
    while True:
        # Check if we're out of labels to search through.
        if table_index >= label_table_index:
            print_buffer()
            print("LABEL NOT FOUND ERROR")
            exit(1)

        # Check if the label is the right size.
        size = label_table[table_index]
        if buffer_index == size:
            loop_index = 1

            # Loop through both the buffer string and the entry's string at the same time.
            while True:
                # If we reach the end of the heap, we have a match (cause they're the same size strings).
                if loop_index == buffer_index:
                    return label_table[table_index + size]

                # If any pair of characters don't match, exit the loop.
                if buffer[loop_index] != label_table[loop_index + table_index]:
                    break

                loop_index += 1

        # Navigate to the next entry in the label table.
        table_index += size
        table_index += 1


def table_index_lookup(key: int, table: list, entry_size: int) -> int:
    """Returns the index of the first entry in 'table' whose first field is 'key.'"""
    index = 0
    while True:
        next_entry_key = table[index]
        if next_entry_key == key:
            return index
        if next_entry_key == NULL:
            return NULL

        index += entry_size


def goto_char(target: int) -> None:
    """Reads from the input until it reaches the 'target' character."""
    char = read_input()
    while char != target:
        if char == STOP_CHAR:
            break
        char = read_input()


def get_next_text() -> None:
    """Reads the next 'important' sequence of characters from input into the buffer"""
    global buffer_index

    # Look for the start of a viable sequence
    while True:
        char = read_input()

        # Check what the character is
        if char == MULTI_LINE_CHAR:
            goto_char(MULTI_LINE_CHAR)
        elif char == COMMENT_CHAR:
            goto_char(NEWLINE_CHAR)
        elif is_char_important(char):
            break

    # If we hit a stop character, just put that in the buffer.
    if char == STOP_CHAR:
        buffer[0] = char
        buffer_index = 1
        return

    # If we reach the character character, just put the next 2 things into the buffer.
    if char == CHAR_CHAR:
        buffer[0] = char
        char = read_input()
        buffer[1] = char
        char = read_input()
        buffer[2] = char
        buffer_index = 3
        return

    # If we reach a string character, put everything up to & including the next string character in the buffer.
    if char == STRING_CHAR:
        index = 0
        while True:
            buffer[index] = char
            index += 1
            char = read_input()

            if char is STRING_CHAR:
                buffer[index] = char
                buffer_index = index + 1
                break
        return

    buffer_index = 0

    # Else, get the rest of the character sequence
    while True:
        buffer[buffer_index] = char
        buffer_index += 1

        char = read_input()

        if char == MULTI_LINE_CHAR:
            goto_char(MULTI_LINE_CHAR)
            break
        elif char == COMMENT_CHAR:
            goto_char(NEWLINE_CHAR)
            break
        elif char == STOP_CHAR:
            break
        elif not is_char_important(char):  # if char is a skip character
            break


def append_string_label() -> None:
    """Adds the buffer to the label_table as a label, but does not assign it a value."""
    global label_table_index
    index = 1

    # Add size+1
    label_table[label_table_index] = buffer_index
    label_table_index += 1

    # Copy in the label string
    while index != buffer_index:
        label_table[label_table_index] = buffer[index]
        label_table_index += 1
        index += 1


def hash_buffer() -> int:
    """Runs the buffer through the hash function."""
    out = 0

    temp = SEL(buffer[2], 6)
    temp = temp << 15
    out = out | temp

    temp = buffer[2] & 0x1f
    temp = temp << 10
    out = out | temp

    temp = buffer[1] & 0x1f
    temp = temp << 5
    out = out | temp

    temp = buffer[0] & 0x1f
    out = out | temp

    return out


def assemble_next_mnemonic(table: list) -> int:
    """
    Fetches and returns the value of the next mnemonic from the given table.

    CANNOT BE USED FOR INSTRUCTIONS.
    """
    global buffer_index

    get_next_text()

    if buffer_index == 2:
        buffer[2] = 0
        buffer_index += 1

    hash_val = hash_buffer()

    index = table_index_lookup(hash_val, table, 2)

    if index == NULL:
        print_buffer()
        print("OPERAND NOT FOUND ERROR")
        raise NameError

    value_index = index + 1
    value = table[value_index]
    return value


def build_tables() -> None:
    """Does the first pass through the file, building the label table."""
    print("Building tables...")  # For debugging, this should be left in.

    global label_table_index
    write_0_to_input()

    program_counter = 0
    while True:
        # Place the next chunk of admissible text into the heap.
        get_next_text()
        first_char = buffer[0]

        # Check what type of admissible string it is.
        if first_char == STOP_CHAR:  # We're done
            break

        elif first_char == LABEL_CHAR:  # It's a label
            # Add the label to the table.
            append_string_label()

            # Add the value to the table.
            label_table[label_table_index] = program_counter
            label_table_index += 1

        elif first_char == REF_CHAR:
            program_counter += 1

        elif first_char == CONST_CHAR:  # It's a constant
            # Add the label to the table.
            append_string_label()

            # Get the constant's text value.
            get_next_text()

            # Get and store the value of the label.
            if buffer[0] == CHAR_CHAR:
                value = buffer[1]
            else:
                value = get_numeric_value()
            label_table[label_table_index] = value
            label_table_index += 1

        elif first_char == CHAR_CHAR:  # It's a character
            program_counter += 1

        elif first_char == STRING_CHAR:  # It's a string
            program_counter += buffer_index - 1

        elif first_char == ARRAY_CHAR:  # It's an empty array
            zeros = label_lookup()
            program_counter += zeros

        elif SEL(first_char, 6) == 0:  # It's a number
            program_counter += 1

        else:  # It's an instruction
            # Hash the instruction, and lookup how many strings we have to skip (unless it's CAL).
            hash_key = hash_buffer()

            # Check if it's a special type of instruction with its own rules.
            if hash_key == CAL_HASH:
                program_counter += 3

            # Else, figure out the number of operands that are associated with it and skip over them.
            else:
                program_counter += 1
                index = table_index_lookup(hash_key, instructions_table, 3)

                # Finds some typos in the first passthrough.
                if index == NULL:
                    print_buffer()
                    print("INSTRUCTION NOT FOUND ERROR")
                    raise NameError

                index_of_bmp = index + 2
                bitmap = instructions_table[index_of_bmp]
                if SEL(bitmap, 2) != 0:
                    get_next_text()
                if SEL(bitmap, 1) != 0:
                    get_next_text()
                if SEL(bitmap, 0) != 0:
                    get_next_text()

    # After we're done, if we're generating a loadable, write the program counter to the first line of output
    if generate_loadable:
        write_output(program_counter)


def assemble() -> None:
    """Does the second pass through the file, translating assembly into machine code."""
    print("Assembling...")  # For debugging, this should be left in.

    write_0_to_input()

    while True:
        # Place the next chunk of admissible text into the heap.
        get_next_text()
        first_char = buffer[0]

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
                value = buffer[1]
                write_output(value)

            elif first_char == STRING_CHAR:  # It's a string.
                index = 0
                while True:
                    index += 1
                    if index == buffer_index - 1:
                        write_output(NULL)
                        break
                    char = buffer[index]
                    write_output(char)

            elif first_char == ARRAY_CHAR:  # It is an empty array, so we make it.
                value = label_lookup()
                num_zeros = 0
                while num_zeros != value:
                    write_output(0)
                    num_zeros += 1

            elif SEL(first_char, 6) == 0:  # It is (probably) a numeric value.
                value = get_numeric_value()
                write_output(value)

            else:  # It's an instruction.
                # Hash the instruction.
                hash_val = hash_buffer()

                # See if it's CAL
                if hash_val == CAL_HASH:
                    write_output(0x3078)  # MOV RA PC
                    write_output(0xb974)  # ALI ADD RA 4
                    write_output(0x4600)  # JIF TRU

                else:
                    # Translate the instruction and get the bitmap.
                    index = table_index_lookup(hash_val, instructions_table, 3)
                    value_index = index + 1
                    out = instructions_table[value_index]
                    bmp_index = value_index + 1
                    bitmap = instructions_table[bmp_index]

                    # Gather operands according to the bitmap.
                    if SEL(bitmap, 2) != 0:
                        value = assemble_next_mnemonic(modifier_table)
                        value = value << 8
                        out = out | value

                    if SEL(bitmap, 1) != 0:
                        value = assemble_next_mnemonic(register_table)
                        value = value << 4
                        out = out | value

                    if SEL(bitmap, 0) != 0:
                        if SEL(bitmap, 3) != 0:
                            get_next_text()
                            value = get_numeric_value()
                            value = value & 0xf
                        else:
                            value = assemble_next_mnemonic(register_table)
                        out = out | value

                    write_output(out)
