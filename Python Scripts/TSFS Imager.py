"""Generates the TSFS drive image for a given directory. Ignores certain files."""


from sys import argv
from os import listdir
from os.path import isfile, isdir
from enum import IntEnum, unique
from modules.hex_interface import read_data_from_hex as read_data
from modules.hex_interface import write_data_to_hex as write_data


@unique
class FileSignature(IntEnum):
    """The file signatures in TSFS"""

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
    DIRECTORY = 0xFD00
    ANYTHING = 0xFFFF


# File types and extensions
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
ignored_exts = ["tasl", "table", "txt", "rtl"]


# Input & output
TOTAL_ARGS = 2
TSFS_EXTENSION = ".tsfs.hex"


# Drive image settings
ENTRY_SIZE = 2  # The size of the tuples in the array. For now it's 2, it may be extended in the future.
EMPTY_TUPLE = (0, 0)  # What empty tuples look like
EXTRA_FILE_SPACE = 0  # The amount of empty space to place after each directory.
EXTRA_INDEX_SPACE = 0  # The number of empty tuples to add to each directory's index.
ENTRY_ADDR = 0
ENTRY_SIG = 1


def main() -> None:
    """
    The first function that runs in the program.

    Raises:
        ValueError: The incorrect number of arguments were provided.
        NotADirectoryError: The given argument was not a directory, or is not a full path.
    """

    # Get input directory
    if len(argv) != TOTAL_ARGS:
        print("Error: Incorrect number of arguments. Expected: " + str(TOTAL_ARGS - 1) +
              ", Actual: " + str(len(argv) - 1))
        raise ValueError
    main_directory = argv[1]

    # Check if directory is not full path
    if not main_directory.startswith('C'):
        print("Error: Main directory needs to be a FULL path, not partial.")
        raise NotADirectoryError

    # Trim the directory
    if main_directory.endswith('"'):
        main_directory = main_directory[:-1]
    if main_directory.endswith('\\'):
        main_directory = main_directory[:-1]

    # Check if the directory exists
    if not isdir(main_directory):
        print("Error: The main directory '" + main_directory + "' does not exist.")
        raise NotADirectoryError

    print("Input directory good, beginning imaging...")
    print("")
    main_directory_data = import_directory_as_TSFS(main_directory)
    print("")
    print("Imaging done, writing to output...")

    # Place the output inside the main directory.
    directory_name = main_directory.split('\\')[-1]
    output_file_path = main_directory + "\\." + directory_name + TSFS_EXTENSION

    write_data(main_directory_data, output_file_path)


def append_to_index(drive_index: list, entry: tuple) -> None:
    """Appends the entry to drive index properly."""

    signature_out = entry[ENTRY_SIG]
    file_addr_out = entry[ENTRY_ADDR]

    drive_index.append(int(file_addr_out))
    drive_index.append(int(signature_out))


def file_signature_of(file_path: str) -> FileSignature:
    """Returns the file signature of the given file."""

    # If this is a directory, return DIRECTORY.
    if isdir(file_path):
        return FileSignature.DIRECTORY

    # If the file's extension is not supported, warn the user and return nothing.
    path_parts = file_path.split('.')
    if path_parts[-1] not in accepted_exts:
        print("Error: '" + file_path + "' has an unsupported file extension.")
        raise TypeError

    # If the file lacks a supported full extension, return ANYTHING.
    full_ext = path_parts[-2] + '.' + path_parts[-1]
    if full_ext not in full_ext_types:
        return FileSignature.ANYTHING

    # If the file has a supported full extension, return its signature.
    return full_ext_types[full_ext]


def import_directory_as_TSFS(directory_path: str) -> [int]:
    """
    Returns TSFS formatted data of the given directory and its subdirectories.

    Raises:
        NotADirectoryError: Given directory is invalid
        TypeError: File found in directory is invalid
    """

    # Check if directory is correct before getting files.
    if not isdir(directory_path):
        print("Error: '" + directory_path + "' is not a valid directory.")
        raise NotADirectoryError
    file_names = listdir(directory_path)

    print("Imaging directory: " + directory_path)

    # Create the variables for generating TSFS lines.
    actual_files = 0  # ...for now
    starting_file_address = 0  # ...for now
    drive_index = []
    drive_file_data = []

    # Loop through each file.
    for file_name in file_names:

        # Get the file's full path
        file = directory_path + "\\" + file_name

        if not file_name.split('.')[-1] in ignored_exts and not file_name.endswith(TSFS_EXTENSION):
            actual_files += 1

            # Get the file's signature.
            signature = file_signature_of(file)

            # Add file information to the directory.
            file_entry = (starting_file_address, signature)
            append_to_index(drive_index, file_entry)
            file_as_data = data_lines_of(file)

            if len(file_as_data) != 0:
                drive_file_data = drive_file_data + file_as_data

                # Increase the file address.
                starting_file_address += len(file_as_data)
        else:
            print("Ignoring: " + file_name)

    # Add the final entry into the index and trailing empty entries.
    append_to_index(drive_index, (starting_file_address, FileSignature.EMPTY))

    for _ in range(EXTRA_INDEX_SPACE):
        append_to_index(drive_index, EMPTY_TUPLE)

    for entry in range(actual_files + 1):
        drive_index[entry * ENTRY_SIZE + ENTRY_ADDR] += len(drive_index)

    # Add trailing 0's to the file data
    drive_file_data + [0] * EXTRA_FILE_SPACE

    # Return the full directory image
    return drive_index + drive_file_data


def data_lines_of(path: str) -> [int]:
    """
    Returns the data at the given path as a list of lines.

    Raises:
        TypeError: The file type is invalid.
        FileNotFoundError: The file does not exist.
    """
    if isdir(path):
        return import_directory_as_TSFS(path)

    if isfile(path):
        file_ext = path.split('.')[-1]
        if file_ext == "hex":
            return read_data(path)
        else:
            print("Error: Unsupported file type: '" + file_ext + "'")
            raise TypeError

    else:
        print("Error: Path '" + path + "'does not exist.")
        raise FileNotFoundError


# Start the program
main()
