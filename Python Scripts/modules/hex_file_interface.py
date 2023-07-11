"""Functions that can be used to read/write .hex files."""

# Output file constants
OUTPUT_FILE_TYPE = ".hex"
HEX_FILE_HEADER = "v2.0 raw\n"
WORDS_PER_LINE = 8
BITS_PER_WORD = 16
FULL_WORD_OUTPUT = True  # Makes output look like this: 0034 10B3 000A instead of 34 10B3 A


def write_data_to_hex(data_list: [int], file_path: str) -> None:
    """Writes the list of signed ints to the file path in .hex format (does not append .hex to name)."""
    out_lines = [HEX_FILE_HEADER]
    words = 0

    for num in data_list:
        if words == 0:
            out_lines.append(format_signed_int(num))
            words += 1
        else:
            out_lines[-1] += (' ' + format_signed_int(num))
            words += 1

        if words == WORDS_PER_LINE:
            out_lines[-1] += '\n'
            words = 0

    if words != 0:
        out_lines[-1] += '\n'

    with open(file_path, 'w') as output_file:
        output_file.writelines(out_lines)


def format_signed_int(value: int) -> str:
    """Returns the .hex encoding of the given signed integer."""
    return normalized_hex(value, int(BITS_PER_WORD/4))[2:]


def read_data_from_hex(file_path: str) -> [int]:
    """Returns a list of numbers from the given hex file."""
    output = []

    with open(file_path, 'r') as input_file:
        input_lines = input_file.readlines()
        input_lines.pop(0)

        for line in input_lines:
            words = line.split(' ')

            for word in words:
                output.append(int("0x" + word, 16))

    return output


def read_text_as_ASCII(file_path: str) -> [int]:
    """Returns the text file contents in ASCII encoded integers."""
    output = []

    with open(file_path, 'r') as input_file:
        input_lines = input_file.readlines()
        for line in input_lines:
            for char in line:
                output.append(ord(char))

    return output


def normalized_hex(value: int, nibbles: int) -> str:
    """
    Formats a given signed integer into a hexadecimal string with exactly the given number of nibbles.

    Raises:
        ValueError: The given value is not valid.
    """
    bits = nibbles*4

    # Convert the value to the correct positive one if negative.
    if value < 0:
        if value < -2**(bits - 1):
            print("\nERROR: Value to low in normalized_hex() (won't be considered negative)\n")
            raise ValueError
        value = value + 2**bits

    # If the value is too big, error.
    if value > 2**bits:
        print("\nERROR: Value too big in normalized_hex().\n")
        raise ValueError

    hex_str = hex(value)[2:]
    num_zeros = nibbles - len(hex_str)
    return "0x" + ('0' * num_zeros) + hex_str
