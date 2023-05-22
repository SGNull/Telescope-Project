"""
Allows users to bundle source code modules with a main file to assemble & debug.

Only takes the "primary" .tasl file as a command line argument.

Produces a .b.tl file containing the contents of the main file and each .tlm file in the same directory.
"""

from sys import argv as args
from os import listdir
from os import remove as delete_file
from os.path import dirname
from os.path import isfile
import modules.assembler_interface as asm_iface
from modules.file_paths import remove_file_extension as remove_ext

MODULE_FILE_EXT = '.tlm'
BUNDLE_PRE_EXT = '.b'
COMPRESSED_EXT = asm_iface.COMPRESSED_FILE_SUFFIX

USAGE_STATEMENT = "Usage: py [script name].py [main file].tasl"


def main() -> None:
    # Check arguments.
    msg = ""
    if len(args) != 2:
        msg = "ERROR: Incorrect number of arguments."
    elif not isfile(args[1]):
        msg = "ERROR: Argument is not a file."

    if msg:
        print(msg)
        print(USAGE_STATEMENT)
        exit(1)

    # Get the main file.
    main_file_path = args[1]
    main_file_directory = dirname(main_file_path)
    name_path = remove_ext(main_file_path)

    # Get the module files in the same directory.
    dir_files = listdir(main_file_directory)
    module_files = [(main_file_directory + '\\' + file) for file in dir_files
                    if file.endswith(MODULE_FILE_EXT) and isfile(main_file_directory + '\\' + file)]

    # Compress the files.
    compress_file(main_file_path)
    temp_files = [name_path + COMPRESSED_EXT]
    for file in module_files:
        compress_file(file)
        temp_files.append(remove_ext(file) + COMPRESSED_EXT)

    # Combine the temp files, then delete them.
    combined_file = name_path + BUNDLE_PRE_EXT + COMPRESSED_EXT
    append_text_files(combined_file, temp_files)
    for file in temp_files:
        delete_file(file)


def append_text_files(output_file: str, files: [str]) -> None:
    """Appends the text of the given files to the given output file."""
    with open(output_file, 'a') as output:
        for file in files:
            if not isfile(file):
                print("ERROR: append_text_files was given a non-file input: ")
                print(file)
                raise FileNotFoundError

            with open(file, 'r') as in_file:
                lines = in_file.readlines()
                output.writelines(lines)


def compress_file(file: str) -> None:
    """Runs the compressor on the given file."""
    interface_args = ["", file, asm_iface.COMPRESS_ARG]
    asm_iface.interface(interface_args)


main()
