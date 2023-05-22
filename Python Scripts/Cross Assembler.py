"""
Runs the assembler interface with the given command line arguments.

Usage:
    py "Cross Assembler.py" [input_file_path](necessary) [mode](optional)

Modes:
    - none -> normal assemble mode (generate TLO file) [NOT RECOMMENDED]
    - -d   -> debug mode (generate RTL and TABL files)
    - -c   -> compress mode (generate TL file)
    - -l   -> loadable mode (generate TLOAD file) [RECOMMENDED]
"""

# This script just runs the assembler interface with the given arguments.

# Developer notes:
# This script is built on top of 3 separate modules (4 including the .hex file interface module):
#   assembler_simulation:   A simulation/emulation of the self-assembler in Python. It *just* does that.
#   enhanced_assembler:     All of the extra features that are specific to the Python cross-assembler.
#   assembler_interface:    Uses the given arguments to instruct enhanced_assembler on how to do cross-assembling.

from modules.assembler_interface import interface
from sys import argv

interface(argv)
