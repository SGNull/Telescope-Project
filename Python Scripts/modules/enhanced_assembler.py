"""
An interface for the assembler_simulation with extra features.

Functions:
    - hash_mnemonic(text) -> int: Use the assembler's hash function on the given mnemonic.
    - assemble(data, is_loadable) -> [int]: Assemble the given data in the given format (loadable or not).
    - gather_labels(data) -> [str]: Get all of the labels and their values from the given data.
    - reduce_data(data, to_RTL) -> [str]: Reduce the given data to RTL or TL.
"""

import modules.assembler_simulation as asm
from modules.hex_interface import normalized_hex


# Hardware determined constant
WORD_BITS = 16

# RTL files begin with this:
RTL_HEADER = "NOTE: DESPITE THEIR APPEARANCE, RTL FILES CANNOT BE ASSEMBLED"


def hash_mnemonic(text: str) -> int:
    """
    Uses the assembler itself to hash the given mnemonic. This ensures the correct hash is used with new mnemonics.

    WARNING: Input text must be only 2 or 3 characters long.
    """
    for idx, char in enumerate(text):
        asm.buffer[idx] = ord(char)

    return asm.hash_buffer()


def assemble(data: [int], is_loadable: bool) -> [int]:
    """
    Runs the assembler on the given raw data [int] and returns the output raw data [int].

    If is_loadable, produces a loadable formatted output, else it just produces machine code.
    """
    __set_input_ROM(data)
    asm.generate_loadable = is_loadable
    asm.start_point()
    print("Done assembling!")
    return asm.output_ROM


def gather_labels(data: [int]) -> [str]:
    """Returns the contents of the label table for the given data [int] as a list of lines."""
    # See the label table structure to better understand how this function works.
    index = 0
    outlines = []

    # Set up the assembler environment for label table gathering.
    __set_input_ROM(data)
    asm.build_tables()

    print("Scanning the label table...")

    # While we're not at the end of the label table,
    while index < asm.label_table_index:
        # Get the size (+1) of the label string
        size = asm.label_table[index]
        # Go to the start of the string and write it into the variable "label"
        index += 1
        label = ""
        for offset in range(0, size - 1):
            label += chr(asm.label_table[index + offset])

        # Now get the value right after the string.
        index += size - 1
        value = asm.label_table[index]

        # Then print the label number, label name, and its value
        outlines.append(normalized_hex(value, int(WORD_BITS / 4)) + " - " + label + "\n")

        # Finally, increment the index for the next label
        index += 1

    print("Done scanning!")
    return outlines


def reduce_data(data: [int], to_RTL: bool) -> [str]:
    """Uses assembler functions to generate a reduced version of the input data [int], either to TL or RTL."""

    # Setup the assembler environment before continuing.
    asm.write_0_to_input()
    __set_input_ROM(data)

    # Setup the output lines for the loop
    outlines = []

    # RTL files should start with an empty line (or comment) to match the Logisim drive line numbers.
    if to_RTL:
        print("Reducing input to RTL...")
        outlines.append(RTL_HEADER + "\n")
    else:
        print("Reducing input to TL...")

    # Loop through the input file again
    while True:
        asm.get_next_text()
        first_char = asm.buffer[0]

        # Stop on STOP_CHAR
        if first_char is asm.STOP_CHAR:
            break

        # Ignore labels if RTL
        elif first_char is asm.LABEL_CHAR:
            # If this does not occur within the elif block, it will treat labels as instructions.
            # ^^^ Seriously. There is an "else" at the bottom of this "elif" chain. Leave this be.
            if not to_RTL:
                outlines.append(asm.buffer_as_string() + "\n")

        # Ignore constants if RTL
        elif first_char is asm.CONST_CHAR:
            temp_string = ""

            if not to_RTL:
                temp_string = asm.buffer_as_string()

            asm.get_next_text()

            if not to_RTL:
                outlines.append(temp_string + " " + asm.buffer_as_string() + "\n")

        # Write everything else to the output.
        elif first_char is asm.CHAR_CHAR:
            temp_string = asm.buffer_as_string()

            # Check for edge-cases if reducing to_RTL
            if to_RTL and temp_string[1] == '\n':
                temp_string = "'\\n'"
            elif to_RTL and temp_string[1] == "'":
                temp_string = "''' \\'"
            elif to_RTL and temp_string[1] == "\t":
                temp_string = "'\\t'"

            outlines.append(temp_string + "\n")

        elif first_char is asm.STRING_CHAR:
            chars = asm.buffer_as_string()[1:-1]

            if to_RTL:
                for char in chars:
                    if char == '\n':
                        outlines.append("'\\n'\n")
                    elif char == "'":
                        outlines.append("''' \\'\n")
                    elif char == "\t":
                        outlines.append("'\\t'\n")
                    else:
                        outlines.append("'" + char + "'\n")
                outlines.append("0xffff\n")
            else:
                outlines.append(asm.buffer_as_string() + "\n")

        elif first_char is asm.REF_CHAR:
            outlines.append(asm.buffer_as_string() + "\n")

        elif chr(first_char).isnumeric():
            outlines.append(asm.buffer_as_string() + "\n")

        # If to_RTL, we want to write all of the zeros to the output
        elif first_char is asm.ARRAY_CHAR:
            if to_RTL:
                num_zeros = asm.label_lookup()
                for i in range(0, num_zeros):
                    outlines.append("0x0000 of " + asm.buffer_as_string()[1:] + " \n")
            else:
                outlines.append(asm.buffer_as_string() + "\n")

        else: # if the buffer contains an instruction
            # This part is mostly a direct copy from build_tables
            instruction = asm.buffer_as_string()

            hash_key = asm.hash_buffer()

            if hash_key == asm.CAL_HASH:
                if to_RTL:
                    outlines.append("CAL (MOV RA PC)\n")
                    outlines.append("|   (ALI ADD RA 4)\n")
                    outlines.append("|   (JMP)\n")
                else:
                    outlines.append("CAL\n")
            else:
                index = asm.table_index_lookup(hash_key, asm.instructions_table, 3)

                bmp_index = index + 2
                bitmap = asm.instructions_table[bmp_index]

                if asm.SEL(bitmap, 2) != 0:
                    asm.get_next_text()
                    instruction += " " + asm.buffer_as_string()
                if asm.SEL(bitmap, 1) != 0:
                    asm.get_next_text()
                    instruction += " " + asm.buffer_as_string()
                if asm.SEL(bitmap, 0) != 0:
                    asm.get_next_text()
                    instruction += " " + asm.buffer_as_string()

                outlines.append(instruction + "\n")

    print("Done reducing!")
    return outlines


def __set_input_ROM(data: [int]) -> None:
    """
    Sets the assembler's input ROM to the given raw data.

    DO NOT USE OUTSIDE OF THIS MODULE
    """
    asm.input_ROM = data
