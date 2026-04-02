# NandToTetris
Repository of my programming solutions for the NAND to Tetris/Building a modern Computer from Scratch course.

#### Context 
"NAND to Tetris: Building a modern computer from first principles" is an online computer science course where participants start with simple NAND logic gates and iteratively build larger and more complex components, with the final goal being to build a basic 16-bit computer. In the next step (Project 6), they use a programming language of their choice to script an assembler that translates the computers assembly language into binaries. 

#### Contents
This repository consists of the assembler which translates .asm files into .bin files, and the project_6 folder containing the test files for it.

#### Solution Approach
The Assembler is written in python and works in the following steps:
1. Read in a .asm file
2. Split it into lines
3. Remove comments and empty lines
4. Based on the first letter of each line (and if necessary second or third letters) differentiate which instruction each line contains. Use that to forward them to the corresponding translation functions.
5. Append output to a new list of binary lines.
6. Join and write to .bin files

This does of course paper over the conversion functions, which are where much of the challenge lies, and which require study of the CPUs documentation, just as building it did.

#### Personal note
I had previously played the puzzle game Turing Complete, in which you also build a simple CPU from scratch, but with very different architecture and consequently assembly instruction sets. This in turn got me to look into other CPU designs, and that emphasized to me just how limited these toy models truly are. Something that might take multiple steps in the minimalist 16 or 8 bit CPUs can be done in 1 step in a modern one. 


