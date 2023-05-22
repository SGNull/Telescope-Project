"""A test hashing program for the assembler."""

from modules.enhanced_assembler import hash_mnemonic
from modules.hex_file_interface import normalized_hex

# Strings that people might input when trying to exit the hash program:
exit_strings = ["exit", "q", "quit", "stop", "halt", "done"]


def main():
    while True:
        mnemonic = input("")

        if len(mnemonic) == 2 or len(mnemonic) == 3:
            hash_val = hash_mnemonic(mnemonic)
            hash_hex = normalized_hex(hash_val, nibbles=4)
            print(hash_hex)

        elif mnemonic.lower() in exit_strings:
            print("Stopping...")
            break

        else:
            print("Input did not have 2 or 3 characters.")


main()
