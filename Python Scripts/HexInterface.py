"""Functions that can be used to read/write .hex files."""

from math import ceil

# Output file constants
OUTPUT_FILE_TYPE = ".hex"
HEX_FILE_HEADER = "v2.0 raw\n"
WORDS_PER_LINE = 8
BITS_PER_WORD = 16
FULL_WORD_OUTPUT = True  # Makes output look like this: 0034 10B3 000A instead of 34 10B3 A


def write_data_to_hex(data_list: [int], file_path: str) -> None:
    """Writes the list of numbers to the file path in .hex format (does not append .hex to name)."""

    out_lines = [HEX_FILE_HEADER]
    words = 0

    for num in data_list:
        if words == 0:
            out_lines.append(format_data(num))
            words += 1
        else:
            out_lines[-1] += (' ' + format_data(num))
            words += 1

        if words == WORDS_PER_LINE:
            out_lines[-1] += '\n'
            words = 0

    if words != 0:
        out_lines[-1] += '\n'

    with open(file_path, 'w') as output_file:
        output_file.writelines(out_lines)


def format_data(value: int) -> str:
    """Returns the .hex encoding of the given integer."""

    if value < 0:
        hex_num = hex(2 ** BITS_PER_WORD + value)[2:]
    else:
        hex_num = hex(value)[2:]

    if FULL_WORD_OUTPUT:
        max_zeros = ceil(BITS_PER_WORD/4)
        zeros = '0' * (max_zeros - len(hex_num))
        return zeros + hex_num
    else:
        return hex_num


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
