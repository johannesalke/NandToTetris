# NandToTetris
Repository of my programming solutions for the NAND to Tetris course.

Context: "NAND to Tetris: Building a modern computer from first principles" is an online computer science course where participants start with simple NAND logic gates and iteratively build larger and more complex components, with the final goal being to build a basic 16-bit computer. In the next step (Project 6), they use a programming language of their choice to script an assembler that translates the computers assembly language into binaries. 

Contents: This repository consists of the programs that translate files into other files (e.g. assembly to binary) and folders with test files for these programs. project_6 has assembly files. project_7 has vm (virtual machine) files. 

Personal notes: After writing the vm-to-asm translator, I looked up up 'real' assembly languages such as x86 look like, and it turns out that most of the features introduced in the vm layer, such as the stack, arithmetic/boolean operations and function definition, all are already encorporated in that assembly language. Partly this seems to be a result of a more versatile CPU. With 32/64 bits and more complex architecture, you can do a lot of things in one operation that would take multiple steps with the hack architecture. But other features, such as the stack being built in, cannot be explained that way. They are true cases of additional abstraction being the default. 


