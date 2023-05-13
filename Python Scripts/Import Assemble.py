"""
Allows users to import source code files before assembling.
Takes two arguments: input file path (necessary), mode (optional)


Takes the "primary" .tasl file as a command line argument.

Considers all .tlm module files in the same directory.
Converts the primary and .tlm files into temporary .tl files.

Appends each .tl file to each other into a temp .tl file.
Runs the assembler on the resulting temp file.
Produces a PrimaryFileName.C.tload file.

Deletes all temporary files.
"""


from sys import argv as args


MODULE_FILE_EXT = '.tlm'

COMPRESS_ALL = '-c'


def main() -> None:
    # Get the main file.
    main_file_path = args[1]
    main_file_directory = '\\'.join(main_file_path.split('\\')[:-1])

    # Get the module files in the same directory.
    dir_files = get_directory_files(main_file_directory)
    module_files = list(filter(
        (lambda f: f.endswith(MODULE_FILE_EXT))
        , dir_files))

    # Compress the files.
    temp_files: [str] = []
    compressed_file = compress_file(main_file_path)
    temp_files.append(compressed_file)
    for file in module_files:
        compressed_file = compress_file(file)
        temp_files.append(compressed_file)

    # Combine the files
    combined_tl = append_text_files(temp_files)

    if len(args) == 3 and args[2] == COMPRESS_ALL:
        delete_files(temp_files)
        return


def get_directory_files(directory: str) -> [str]:
    pass


def append_text_files(files: [str]) -> str:
    pass


def compress_file(file: str) -> str:
    pass


def assemble_file(file: str) -> str:
    pass


def delete_files(files: [str]) -> None:
    pass


main()
