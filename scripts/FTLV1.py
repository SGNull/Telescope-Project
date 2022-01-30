"""
Usage: FTLV1.py InputFile (optional OutputFile defaults to InputFile.lmem)

This is a converter that takes a text file as input, and outputs an unpacked ASCII Logisim drive image.
The specific drive dimensions are: 8-bit words x N-bit addressing.
It will create the output file if the one specified is not found, or if only the input file is specified.
"""

# Module imports
import sys  # For file arguments

# File name constants
CONVERTER_FILE_NAME = "FTLV1.py"
OUTPUT_FILE_TYPE = ".lmem"

# Important translation constants
OUTPUT_EOF = "0"
LOGISIM_FILE_HEADER = "v2.0 raw"

# Exit codes
CLI_EXIT_CODE = 2
GEN_EXIT_CODE = 1
GOOD_EXIT_CODE = 0

# List of characters to replace:
REPLACE_CHARS = {
    '\t': "    "
}


def char_to_output(char, output_list):
    """Appends a character to the output in the correct format"""
    ascii_value = ord(char)
    formatted_char = hex(ascii_value)[2:]
    output_list.append(formatted_char + "\n")


def validate_args():
    """Checks if we have the right arguments"""
    if len(sys.argv) > 3 or len(sys.argv) < 2:
        print("Invalid number of arguments. Expected 1 or 2 arguments but instead got " + str(len(sys.argv)))
        print("Usage: " + CONVERTER_FILE_NAME + " InputFile.ext (optional OutputFile)")
        exit(CLI_EXIT_CODE)


def file_translator(input_file, output_list):
    """The actual file translator. Sends the translation to the output list."""
    char = input_file.read(1)
    while char:
        if char in REPLACE_CHARS:  # Replace the character
            for sub_char in REPLACE_CHARS[char]:
                char_to_output(sub_char, output_list)
        else:  # Translate the character
            char_to_output(char, output_list)

        # Go to next character
        char = input_file.read(1)


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

    # Open the files at the same time to avoid errors
    with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
        # Create the output_list
        output_list = [LOGISIM_FILE_HEADER + "\n"]

        # Translate the input_file
        file_translator(input_file, output_list)

        # Append EOF to the output_list
        output_list.append(OUTPUT_EOF + "\n")

        # Now write the values in output_list to the output_file
        output_file.writelines(output_list)


# Run main()
main()
