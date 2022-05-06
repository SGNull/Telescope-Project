# Takes multiple files as input, and creates a new TSFS drive image in the current directory
# Usage:  TSFS Drive Image Creator.py  OutputFileName,  InputFilePath1,  InputFilePath2,  ...


import sys
from os.path import exists


full_ext_types = {
    "dat.hex": 1,
    "txt.hex": 2,
    "tlo.hex": 3,
    "tload.hex": 4,
    "tasl.hex": 5,
    "tl.hex": 6
}
accepted_exts = ["hex"]

output_image_files = []
output_TSFS_array = []


file_paths = []
if len(sys.argv) < 2:
    print("Need at least an output file to run.")
    exit(1)
elif len(sys.argv) > 2:
    file_paths = sys.argv[2:]

current_files_address = len(file_paths) * 2


for file_path in file_paths:
    file_ext = file_path.split('.')[-1]

    if file_ext not in accepted_exts:
        print("Error, file type not supported: " + file_path)
        exit(1)

    if not exists(file_path):
        print("Error, file does not exist: " + file_path)
        exit(1)

    file_sig = 0xFFFF
    for ext in full_ext_types:
        if file_path.endswith(ext):
            file_sig = full_ext_types[ext]
            break

    output_TSFS_array.append(file_sig)
    output_TSFS_array.append(current_files_address)

    with open(file_path, 'r') as input_file:
        lines = input_file.readlines[1:]
        output_image_files = output_image_files + lines
        current_files_address += len(lines)

output_lines = ["v2.0 raw"] + output_TSFS_array + output_image_files
with open(sys.argv[1], 'w') as output_file:
    output_file.writelines(output_lines)
