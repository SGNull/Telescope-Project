"""Allows users to view the contents of TSFS drives easily."""


from sys import argv
from os.path import isfile
from enum import IntEnum, unique
from HexInterface import read_data_from_hex as read_data
from HexInterface import format_data


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


signature_names = {
    FileSignature.EMPTY: "Empty",
    FileSignature.ANY_DATA: "Data",
    FileSignature.ANY_TEXT: "Text",
    FileSignature.MACHINE_CODE: "Machine Code",
    FileSignature.LOADABLE_CODE: "Loadable",
    FileSignature.SOURCE_CODE: "Source Code",
    FileSignature.COMPRESSED_CODE: "Compressed Code",
    FileSignature.DIRECTORY: "Directory",
    FileSignature.ANYTHING: "Non-Empty"
}

TSFS_FILE_EXTENSION = ".tsfs.hex"

ENTRY_SIZE = 2
ENTRY_ADDR = 0
ENTRY_SIG = 1

TOTAL_ARGS = 2

exit_strings = ["exit", "quit", "stop", "end", "q"]

WORDS_PER_OUT_LINE = 8  # For printing file contents


def main() -> None:
    """The first function that runs in the program."""

    # Get TSFS file
    if len(argv) != TOTAL_ARGS:
        print("Error: Incorrect number of arguments. Expected: " + str(TOTAL_ARGS - 1) +
              ", Actual: " + str(len(argv) - 1))
        raise ValueError
    drive_image_path = argv[1]

    # Check if TSFS path is correct
    if not isfile(drive_image_path):
        print("Error: File '" + drive_image_path + "'does not exist.")
        raise FileNotFoundError

    if not drive_image_path.endswith(TSFS_FILE_EXTENSION):
        print("Error: Not a TSFS file.")
        raise TypeError

    drive_image_data = read_data(drive_image_path)

    if len(drive_image_data) == 0:
        print("Read nothing from drive image.")
        exit(0)

    index_size = get_entry(drive_image_data, 0)[ENTRY_ADDR]
    drive_index = drive_image_data[:index_size]
    drive_files = drive_image_data[index_size:]

    # Print the index contents, and begin the UI
    print_index(drive_index)
    print("")
    print("--------------------")
    print("")
    while True:
        entry_num = input("Enter the entry number to view the data of: ")

        if entry_num.lower() in exit_strings:
            break
        elif not entry_num.isdigit():
            print("Input was not a number.")
        elif int(entry_num) not in range(int(index_size/ENTRY_SIZE)):
            print("Entry out of bounds.")
        else:
            entry = get_entry(drive_index, int(entry_num))
            if entry[ENTRY_SIG] == FileSignature.EMPTY:
                print("Entry is of empty file.")

            # elif entry[0] == FileSignature.DIRECTORY:
            #     print("Entering directory...")
            #     --enter directory code here--

            else:
                next_entry = get_entry(drive_index, int(entry_num) + 1)
                print("Printing file data...")
                print("")
                file_start_index = entry[ENTRY_ADDR] - index_size
                file_end_index = next_entry[ENTRY_ADDR] - index_size

                buffer = []
                for i in range(file_start_index, file_end_index):
                    buffer.append(format_data(drive_files[i]))
                    if len(buffer) == WORDS_PER_OUT_LINE:
                        print_list(buffer)
                        buffer = []
                if len(buffer) != 0:
                    print_list(buffer)

        print("")


def print_index(drive_index: list) -> None:
    """Prints the drive's index in a user-friendly format."""
    print("Printing drive index...")
    print("")

    if len(drive_index) % ENTRY_SIZE != 0:
        print("Error: Bad drive index size.")
        raise ValueError

    num_entries = int(len(drive_index) / ENTRY_SIZE)
    for index in range(num_entries):
        entry = get_entry(drive_index, index)
        print("Entry " + str(index) + ": " + signature_names[entry[ENTRY_SIG]] + ",  " + hex(entry[ENTRY_ADDR]))


def get_entry(drive_index: [int], entry_num: int) -> (int, int):
    """Returns the given numbered entry in the given drive index."""
    entry_pt1 = drive_index[entry_num * ENTRY_SIZE]
    entry_pt2 = drive_index[entry_num * ENTRY_SIZE + 1]
    entry = (entry_pt1, entry_pt2)
    return entry


def print_list(my_list: list) -> None:
    """Prints the list cleanly."""
    print(str(my_list)[1:-1].translate({ord("'"): None, ord(','): None}))


# Start the program
main()
