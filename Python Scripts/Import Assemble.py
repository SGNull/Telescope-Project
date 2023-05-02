"""
Allows users to import source code files before assembling.

Takes the "primary" .tasl file as a command line argument.
Considers all .tlm module files in the same directory.
Converts the primary and .tlm files into temporary .tl files.
Appends each .tl file to each other.
Runs the assembler on the resulting file.
Produces a PrimaryFileName.C.tload file.
Deletes all temporary .tl files.
"""


def main():
    pass


def get_directory_files(directory):
    pass


def append_text_files(files):
    pass


def compress_file(file):
    pass


def assemble_file(file):
    pass


main()
