"""
The interface for the assembler for the Telescope Assembly Light language.

Usage:
    args = [name](not read), [valid input file path](necessary), [mode](optional)
        OR (RECOMMENDED)
    args = sys.argv

    ca_interface.interface(args)

Modes:
    - none -> normal assemble mode (generate TLO file) [NOT RECOMMENDED]
    - -d   -> debug mode (generate RTL and TABL files)
    - -c   -> compress mode (generate TL file)
    - -l   -> loadable mode (generate TLD file) [RECOMMENDED]
"""

# The interface was made separate from the main cross-assembler script so that Import Assembler could use it too.
# The idea is: for each way a user could interact with one file, they could import and assemble multiple files.

from os.path import isfile
import modules.hex_file_interface as hex_iface
import modules.enhanced_assembler as e_asm
from modules.file_paths import remove_file_extension as remove_ext

# Args constants
DEBUG_ARG = "-d"
COMPRESS_ARG = "-c"
LOADABLE_ARG = "-l"
DEFAULT_MODE = '-a'

# For printing
modes_dict = {
    DEBUG_ARG: "debug",
    COMPRESS_ARG: "compress",
    LOADABLE_ARG: "loadable",
    DEFAULT_MODE: "assemble"
}

# File constants:
MACHINE_CODE_EXT = ".tlo.hex"
TABLE_FILE_EXT = ".tabl"
REDUCED_FILE_EXT = ".rtl"
COMPRESSED_FILE_EXT = ".tl"
LOADABLE_FILE_EXT = ".tld.hex"
ACCEPTED_IN_EXT = [".tasl", COMPRESSED_FILE_EXT]

# Hardware Constants:
NULL = 0xFFFF
WORD_BITS = 16


def interface(args) -> None:
    """The main function. Uses the arguments provided to run the assembler in the specified configuration."""

    # Check that the arguments are correct.
    if not args_are_correct(args):
        print('Arguments are incorrect.')
        print('Arguments (in order): [valid input file path](necessary) [mode](optional)')
        print('Valid input file types: ' + str(ACCEPTED_IN_EXT)[1:-1])  # Trimmed unnecessary brackets.
        exit(1)

    # Get the arguments.
    if len(args) == 2:
        mode = DEFAULT_MODE
    else:
        mode = args[2]
    file_path = args[1]

    # Get the input file data.
    file_name_path = remove_ext(file_path)
    file_data = hex_iface.read_text_as_ASCII(file_path) + [0, 0]  # Simulating empty space after data.

    if len(file_data) == 0:
        print("Missing/Empty input file.")
        exit(1)

    # Run the assembler in the given mode.
    run_assembler(mode, file_data, file_name_path)
    print("\nThe simulation has finished.")


def write_to_file(file_path: str, lines: [str]) -> None:
    """Simply writes to the output file, and prints before and after if the file was opened successfully."""
    with open(file_path, 'w') as output_file:
        print("Writing to output file...")
        output_file.writelines(lines)
        print("Done writing to output file!")


# I have the nagging suspicion that this function could be much shorter.
def args_are_correct(sys_args: list) -> bool:
    """Returns whether the arguments are correct."""

    # Check to see if the mode is right if one is provided
    if len(sys_args) == 3:
        if sys_args[2] not in modes_dict:
            return False

    # Check to make sure that the file is correct
    if len(sys_args) == 2 or len(sys_args) == 3:
        input_file_path = sys_args[1]
        if not isfile(input_file_path):
            return False

        return any(input_file_path.endswith(ext) for ext in ACCEPTED_IN_EXT)

    # Else we have the wrong number of arguments
    else:
        return False


def run_assembler(mode: str, input_data: [int], file_name_path: str) -> None:
    """Run the assembler in the given mode, with the given data, and outputting to file_name_path."""
    print("Running in  " + modes_dict[mode].upper() + "  mode.\n")

    if mode == COMPRESS_ARG:
        # Compress the file.
        tl_lines = e_asm.reduce_data(input_data, to_RTL=False)
        output_file_path = file_name_path + COMPRESSED_FILE_EXT
        write_to_file(output_file_path, tl_lines)

    elif mode == DEBUG_ARG:
        # First, make the table file
        labels = e_asm.gather_labels(input_data)
        tbl_output_path = file_name_path + TABLE_FILE_EXT
        write_to_file(tbl_output_path, labels)

        print("\n")  # TWO newlines; Prints newline on a new line.

        # Now make the RTL file
        rtl_lines = e_asm.reduce_data(input_data, to_RTL=True)
        rtl_output_path = file_name_path + REDUCED_FILE_EXT
        write_to_file(rtl_output_path, rtl_lines)

    else:
        # Assemble into machine code.
        loadable = (mode == LOADABLE_ARG)
        machine_code = e_asm.assemble(input_data, loadable)

        if loadable:
            suffix = LOADABLE_FILE_EXT
        else:
            suffix = MACHINE_CODE_EXT
        output_file_path = file_name_path + suffix

        print("Writing to output file...")
        hex_iface.write_data_to_hex(machine_code, output_file_path)
        print("Done writing to output file!")
