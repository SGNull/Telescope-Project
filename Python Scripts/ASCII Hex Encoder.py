"""
Usage: FTLV1.py InputFile (optional OutputFile defaults to InputFile.hex)

This is a converter that takes a text file as input, reads it as ASCII encoding, and outputs a .hex drive image.
It will create the output file if the one specified is not found, or if only the input file is specified.
"""

# Module imports
import sys  # For file arguments
import modules.hex_file_interface as hex_interface

# File name constants
CONVERTER_FILE_NAME = "FTLV1.py"
OUTPUT_FILE_TYPE = ".hex"


def main():
    """The main function for the module."""
    # First, make sure we have the right arguments
    print("Checking args...")
    validate_args()

    # Then get the arguments
    input_file_path = sys.argv[1]
    if len(sys.argv) == 3:
        output_file_path = sys.argv[2]
    else:
        output_file_path = input_file_path + OUTPUT_FILE_TYPE

    # Now use the hex interface module to do all the work for us!
    print("Reading the text...")
    data = hex_interface.read_text_as_ASCII(input_file_path)
    print("Writing the data...")
    hex_interface.write_data_to_hex(data, output_file_path)
    print("Done!")


def validate_args():
    """Checks if we have the right arguments"""
    if len(sys.argv) > 3 or len(sys.argv) < 2:
        print("Invalid number of arguments. Expected 1 or 2 arguments but instead got " + str(len(sys.argv)))
        print("Usage: " + CONVERTER_FILE_NAME + " InputFile.ext (optional OutputFile)")
        exit(1)


# Run main()
main()
