"""A test hashing program for the assembler."""


def main():
    while True:
        mnemonic = input("")
        if len(mnemonic) == 2:
            mnemonic = mnemonic + chr(0)

        if len(mnemonic) == 3:
            out = 0
            temp = ord(mnemonic[2]) & 0x40
            temp = temp << 9
            out = out | temp
            temp = ord(mnemonic[2]) & 0x1F
            temp = temp << 10
            out = out | temp
            temp = ord(mnemonic[1]) & 0x1F
            temp = temp << 5
            out = out | temp
            temp = ord(mnemonic[0]) & 0x1F
            out = out | temp
            print(mnemonic + " - " + hex(out))

        elif mnemonic == "EXIT":
            print("Stopping...")
            break

        else:
            print("Input did not have 3 characters.")


main()
