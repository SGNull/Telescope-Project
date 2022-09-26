"""
Usage: FTLV1.py InputFile (optional OutputFile defaults to InputFile.hex)

This is a converter that takes a text file as input, and outputs an unpacked ASCII Logisim drive image.
The specific drive dimensions are: 8-bit words x N-bit addressing.
It will create the output file if the one specified is not found, or if only the input file is specified.
"""

# Module imports
import sys  # For file arguments
from HexInterface import write_data_to_hex as write_data

# File name constants
CONVERTER_FILE_NAME = "FTLV1.py"
OUTPUT_FILE_TYPE = ".hex"

# Important translation constants
OUTPUT_EOF = "0"
LOGISIM_FILE_HEADER = "v2.0 raw"

# Exit codes
CLI_EXIT_CODE = 2
GEN_EXIT_CODE = 1
GOOD_EXIT_CODE = 0

# Output file constants
WORDS_PER_LINE = 8
FULL_WORD_OUTPUT = True  # Makes output look like this: 0034 10B3 000A instead of 34 10B3 A

# List of characters to replace:
REPLACE_CHARS = {

}


def validate_args():
    """Checks if we have the right arguments"""
    if len(sys.argv) > 3 or len(sys.argv) < 2:
        print("Invalid number of arguments. Expected 1 or 2 arguments but instead got " + str(len(sys.argv)))
        print("Usage: " + CONVERTER_FILE_NAME + " InputFile.ext (optional OutputFile)")
        exit(CLI_EXIT_CODE)


def lines_to_int(input_file) -> [int]:
    """Returns the list of integers representing the characters in the given file."""

    output = []

    # Read file character by character
    char = input_file.read(1)
    while char:

        # Append the replacement
        if char in REPLACE_CHARS:
            for sub_char in REPLACE_CHARS[char]:
                output.append(ord(sub_char))

        # Translate the character
        else:
            output.append(ord(char))

        # Go to next character
        char = input_file.read(1)

    return output


def main():
    """The main function for the module."""
    # First, make sure we have the right arguments
    validate_args()

    # Then get the arguments
    input_file_path = sys.argv[1]
    if len(sys.argv) == 3:
        output_file_path = sys.argv[2]
    else:
        output_file_path = input_file_path + OUTPUT_FILE_TYPE

    # Then send the data to the output
    with open(input_file_path, 'r') as input_file:
        data = lines_to_int(input_file)
        write_data(data, output_file_path)


# Run main()
main()
