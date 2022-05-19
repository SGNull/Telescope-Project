# Takes multiple files as input, and creates a new TSFS drive image in the current directory
# Usage:  TSFS Drive Image Creator.py  OutputFile,  InputFilePath1,  InputFilePath2,  ...


import sys
from os.path import exists
from enum import IntEnum, unique


# The file signatures in TSFS
@unique
class FileSignature(IntEnum):
    # Nice fix from Martijn Pieters on Stack Overflow
    # Makes sure that each time an attribute is used as a string, it evaluates to its value instead of its name
    def __str__(self):
        return str(self.value)

    EMPTY = 0
    ANY_DATA = 1
    ANY_TEXT = 2
    MACHINE_CODE = 3
    LOADABLE_CODE = 4
    SOURCE_CODE = 5
    COMPRESSED_CODE = 6
    ANYTHING = 0xFFFF


# If the file has a "full" extension, we'll automatically add the correct file signature to it's tuple instead of 0xFFFF
full_ext_types = {
    "dat.hex": FileSignature.ANY_DATA,
    "txt.hex": FileSignature.ANY_TEXT,
    "tlo.hex": FileSignature.MACHINE_CODE,
    "tload.hex": FileSignature.LOADABLE_CODE,
    "tasl.hex": FileSignature.SOURCE_CODE,
    "tl.hex": FileSignature.COMPRESSED_CODE
}
accepted_exts = ["hex"]  # For now, all input files must be .hex files.

HEX_FILE_HEADER = "v2.0 raw\n"

ARGS_INPUT_START = 2  # The start of the input file arguments in sys.argv.
MINIMUM_ARGS = 2  # The minimum number of arguments you can pass to this program.


ARRAY_TUPLE_SIZE = 2  # The size of the tuples in the array. For now it's 2, it may be extended in the future.
NUM_IMPORTANT_TUPLES = 1  # The number of important end tuples
NUM_EMPTY_TUPLES = 0  # The number of empty tuples at the end of the array (for adding files to the drive)
EMPTY_TUPLE = (0, 0)  # What empty tuples look like

TSFS_array_lines = []  # The TSFS array at the beginning of a TSFS drive.
TSFS_files_lines = []  # The file segment of the TSFS drive.


def TSFS_array_append(array_entry):
    """Appends the tuple to TSFS_array_lines"""
    global TSFS_array_lines, TSFS_files_lines

    signature_out = hex(array_entry[0])[2:]
    file_addr_out = hex(array_entry[1])[2:]

    TSFS_array_lines.append(signature_out + '\n')
    TSFS_array_lines.append(file_addr_out + '\n')


def main():
    """The main function for the drive image creator"""
    global TSFS_array_lines, TSFS_files_lines

    # Grabbing the input .hex files
    file_paths = []
    if len(sys.argv) < MINIMUM_ARGS:
        print("Need at least an output file to run.")
        exit(0)
    elif len(sys.argv) > MINIMUM_ARGS:
        file_paths = sys.argv[ARGS_INPUT_START:]

    current_files_address = (len(file_paths) + NUM_IMPORTANT_TUPLES + NUM_EMPTY_TUPLES) * ARRAY_TUPLE_SIZE

    # Loop through the input files
    for file_path in file_paths:
        file_ext = file_path.split('.')[-1]

        # Error checks to make sure this input is correct.
        if not exists(file_path):
            print("Error, file does not exist: " + file_path)
            exit(0)

        if file_ext not in accepted_exts:
            print("Error, file type not supported: " + file_path)
            exit(0)

        # Get the correct file signature if it has a "full" file extension.
        file_sig = FileSignature.ANYTHING
        for ext in full_ext_types:
            if file_path.endswith(ext):
                file_sig = full_ext_types[ext]
                break

        # Add the tuple to the array
        array_entry = (file_sig, current_files_address)
        TSFS_array_append(array_entry)

        # Add the file contents to the files list (note: due to the checks above, this always runs)
        with open(file_path, 'r') as input_file:
            lines = input_file.readlines()[1:]
            if not lines[-1].endswith('\n'):
                lines[-1] += '\n'
            TSFS_files_lines += lines
            current_files_address += len(lines)

    # Once we're done, add the ending tuples to the array
    end_tuple = (FileSignature.EMPTY, current_files_address)
    TSFS_array_append(end_tuple)
    for _ in range(0, NUM_EMPTY_TUPLES):
        TSFS_array_append(EMPTY_TUPLE)

    # Now create and write the output
    output_lines = [HEX_FILE_HEADER] + TSFS_array_lines + TSFS_files_lines
    with open(sys.argv[1], 'w') as output_file:
        output_file.writelines(output_lines)


main()
