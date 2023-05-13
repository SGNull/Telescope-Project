"""
The interface for the assembler for the Telescope Assembly Light language.

Arguments:
    [valid input file path](necessary) [mode](optional)

Modes:
    - none -> normal assemble mode (generate TLO file) [NOT RECOMMENDED]
    - -d   -> debug mode (generate RTL and TABL files)
    - -c   -> compress mode (generate TL file)
    - -l   -> loadable mode (generate TLOAD file) [RECOMMENDED]
"""

import sys
import modules.hex_interface as hex_interface
import modules.enhanced_assembler as e_asm


# Args constants
DEBUG_ARG = "-d"
COMPRESS_ARG = "-c"
LOADABLE_ARG = "-l"
modes_dict = {
    DEBUG_ARG: "debug",
    COMPRESS_ARG: "compress",
    LOADABLE_ARG: "loadable"
}

# File constants:
MACHINE_CODE_SUFFIX = ".tlo.hex"
TABLE_FILE_SUFFIX = ".table"
REDUCED_FILE_SUFFIX = ".rtl"
COMPRESSED_FILE_SUFFIX = ".tl"
LOADABLE_FILE_SUFFIX = ".tload.hex"

ACCEPTED_IN_SUFFIX = ["tasl", "tl", "tlm"]

# Hardware Constants:
NULL = 0xFFFF
WORD_BITS = 16


def main() -> None:
    """Uses the arguments provided via the command line to run the assembler in the specified configuration."""

    # Check that the arguments are correct.
    if not args_are_correct(sys.argv):
        print('Arguments are incorrect.')
        print('Arguments (in order): [valid input file path](necessary) [mode](optional)')
        print('Valid input file types: ' + str(ACCEPTED_IN_SUFFIX)[1:-1])  # Trimmed unnecessary brackets.
        exit(1)

    # Get the arguments.
    if len(sys.argv) == 2:
        mode = "default"
    else:
        mode = modes_dict[sys.argv[2]]
    file_path = sys.argv[1]

    # Get the input file data.
    file_name_path = '.'.join(file_path.split('.')[:-1])
    file_data = hex_interface.read_text_as_ASCII(file_path) + [0, 0]  # Simulating empty space after data.

    if len(file_data) == 0:
        print("Missing/Empty input file.")
        exit(1)

    # Run the assembler in the given mode.
    run_operation(mode, file_data, file_name_path)
    print("")
    print("The simulation has finished.")


def write_to_file(file_path: str, lines: [str]) -> None:
    """Simply writes to the output file, and prints before and after if the file was opened successfully."""
    with open(file_path, 'w') as output_file:
        print("Writing to output file...")
        output_file.writelines(lines)
        print("Done writing to output file!")


def args_are_correct(sys_args: list) -> bool:
    """Returns whether the arguments are correct."""
    if len(sys_args) == 3:
        if sys_args[2] not in modes_dict:
            return False

    if len(sys_args) == 2 or len(sys_args) == 3:
        input_file_path = sys_args[1]
        input_file_suffix = input_file_path.split('.')[-1]
        return input_file_suffix in ACCEPTED_IN_SUFFIX

    else:
        return False


def run_operation(mode: str, input_data: [int], file_name_path: str) -> None:
    """Run the assembler in the given mode, with the given data, and outputting to file_name_path."""

    print("Running in " + mode + " mode...")
    loadable = (mode == "loadable")

    if mode == "compress":
        # Compress the file.
        tl_lines = e_asm.reduce_data(input_data, to_RTL=False)
        output_file_path = file_name_path + COMPRESSED_FILE_SUFFIX
        write_to_file(output_file_path, tl_lines)

    elif mode == "debug":
        # First, make the table file
        labels = e_asm.gather_labels(input_data)
        tbl_output_path = file_name_path + TABLE_FILE_SUFFIX
        write_to_file(tbl_output_path, labels)

        print("")

        # Now make the RTL file
        rtl_lines = e_asm.reduce_data(input_data, to_RTL=True)
        rtl_output_path = file_name_path + REDUCED_FILE_SUFFIX
        write_to_file(rtl_output_path, rtl_lines)

    else:
        # Assemble into machine code.
        machine_code = e_asm.assemble(input_data, loadable)

        if loadable:
            suffix = LOADABLE_FILE_SUFFIX
        else:
            suffix = MACHINE_CODE_SUFFIX
        output_file_path = file_name_path + suffix

        print("Writing to output file...")
        hex_interface.write_data_to_hex(machine_code, output_file_path)
        print("Done writing to output file!")


# Begin this entire script by calling main.
main()
