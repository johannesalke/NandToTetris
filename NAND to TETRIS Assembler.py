

#This script has 4 parts:
#1. Function definition,
#2. Reading in the .asm assembly file and pre-processing it to remove comments, leading spaces, etc
#3. translation into binary (using functions).
#4. Combining the individual lines of binary and writing them to a .bin file.

#Note: The various print() commands are a remainder from development I have chosen not to delete. 

#Constructs a C-instruction from its component flags. The following 3 functions are components of this one.
def C_constructor(C6,D3,J3):
    A=''
    if C6.find('M') != -1:
        A = '1'
    else:
        A = '0'
    
    return '111' + A + comp_decoder(C6) +  dest_decoder(D3) + jmp_decoder(J3) 
    

#Translates computational instructions into the corresponding 6-bit binary, which then goes to the C_constructor.
def comp_decoder(cc):
    
#Differentiate between A = 0 and A = 1 for determining whether the second input is A or M.
    if cc == '0':
        return('101010')
    elif cc == '1':
        return('111111')
    elif cc == '-1':
        return('111010')
    elif cc == 'D':
        return('001100')
    elif cc == 'A' or cc == 'M':
        return('110000')
    elif cc == '!D':
        return('00qq0q')
    elif cc == '!A' or cc == '!M':
        return('110001')
    elif cc == '-D':
        return('001111')
    elif cc == '-A' or cc == '-M':
        return('110011')
    elif cc == 'D+1':
        return('011111')
    elif cc == 'A+1' or cc == 'M+1':
        return('110111')
    elif cc == 'D-1':
        return('001110')
    elif cc == 'A-1' or cc == 'M-1':
        return('110010')
    elif cc == 'D+A' or cc == 'D+M':
        return('000010')
    elif cc == 'D-A' or cc == 'D-M':
        return('010011')
    elif cc == 'A-D' or cc == 'M-D':
        return('000111')
    elif cc == 'D&A' or cc == 'D&M':
        return('000000')
    elif cc == 'D|A' or cc == 'D|M':
        return('010101')

    

#Where the computation result is written, if anywhere. A reg, D reg, M reg


def dest_decoder(dd):
    dest = ''
    if dd.find('A') != -1:
        dest = dest + '1'
    else:
        dest = dest + '0'
    if dd.find('D') != -1:
        dest = dest + '1'
    else:
        dest = dest + '0'
    if dd.find('M') != -1:
        dest = dest + '1'
    else:
        dest = dest + '0'
    return dest



# Jump instructions based on comparison flags.
def jmp_decoder(jj):
    if jj == 'JGT':
        return '001'
    elif jj == 'JEQ':
        return '010'
    elif jj == 'JGE':
        return '011'
    elif jj == 'JLT':
        return '100'
    elif jj == 'JNE':
        return '101'
    elif jj == 'JLE':
        return '110'
    elif jj == 'JMP':
        return '111'
    else:
        return '000'









#2. Opening the file and splitting it into lines, saved into a list.

#Asks the user to enter the name of the file to be assembled (without file extension).
fname = input()

  
with open("project_6/"+ fname+ ".asm", "r") as assembly:
    asm = assembly.read()
    asmlist = asm.splitlines()
    #print(asmlist)


#2.1: Remove empty strings.
asmlist = [x for x in asmlist if x.strip()]

#2.2: Remove leading and tracing spaces. 
list2 = []
for i in asmlist:   
    list2.append(i.strip())

asmlist = list2

#print(asmlist)

#2.3: Remove comments
asmlist = [ x for x in asmlist if "/" not in x ]

    

#print(asmlist)


#2.4 Setting up a symbolic adress directory using a dictionary.
#There are subdivisions of symbolics, and they can be found in the project 4 handbook, pg 13.
            #R0 -R15: RAM 0 to RAM 15
            #SP, LCL, ARG, THIS, THAT <=> RAM 0-4
            #SCREEN: RAM 16384, KBD: RAM 24576
            #Userdefined labels. 
            #Variables: Any userdefined symbol not defined elsewhere is given...
            # a unique RAM address by the assembler, starting at R15.
            #=>First step must be to assign addresses to Userlabels. Then Assign them to Variables.
            #Then, you can actually start doing this properly.
            #Also: This assignment can be done before the interpretation. 


symbolic = {}

#Defining R0 to R15
for i in range(0,16):
    ram = 'R'+str(i)
    symbolic[ram] = i

#Defining the pointer registers.
predef = ['SP','LCL','ARG','THIS','THAT']

for i in range(0,5):
    pd = predef[i]
    symbolic[pd] = i

#Defining I/O registers
symbolic['SCREEN'] = 16384
symbolic['KBD'] = 24576




#Defining jump locations, recognized by starting with an open bracket.
inc = 0
for i in range(0,len(asmlist)):
    
    if asmlist[i][0]== '(':
        symbolic[asmlist[i][1:len(asmlist[i])-1]] = i - inc
        inc = inc+1
        

#Undefined variables. Are assigned to RAM addresses 16 and upwards on first use in the program.
free_ram = 16

for instr in asmlist:
    if instr[0] == '@':
        if instr[1:(len(instr))] not in symbolic.keys():
            symbolic[instr[1:(len(instr))]] = free_ram
            free_ram = free_ram + 1
















#3. Translation to binary by running a 'for i in list' loop, which can distinguish between command types. 



binlist = []

for i in range(0,len(asmlist)):
    #getting the length of each instruction for the purpose of cutting the string into its components.
    ilength = len(asmlist[i])
    
    if asmlist[i][0]== '@':
        #Address. Next, distinguishe between tags and symbolic ones based on what the first character after the @ is.
         
         if asmlist[i][1].isdigit():
            
            #print('A-normal')
            binstr = format(int(asmlist[i][1:ilength]),'b')
            binstr = (16 - len(binstr))*'0' + binstr
            binlist.append(binstr)
            #print(binstr)
            
              
         else:
            instr = asmlist[i][1:len(asmlist[i])]
            s_number = symbolic[instr]

            binstr = format(int(s_number),'b')
            binstr = (16 - len(binstr))*'0' + binstr
            binlist.append(binstr)
            #print(binstr)

             
            #print('A-symbolic')

                
        
    elif asmlist[i][0]== '/':
        #Comment. Don't do anything.
        #print('comment')
        ##This was a test case from early development to check whether my if/else tree could properly distinguish the instruction types.
        continue
        
    elif asmlist[i][0]== '(':
        #print('symbolic')
        ##This was a test case from early development to check whether my if/else tree could properly distinguish the instruction types.
        continue
        
    else:
        #If none of the above, it's a C instruction.
        #Seperate the three possible parts of it, and decrypt each into 
        #its own  binary by calling a function from below. 
        #print('C-instruction')
        #Jump instructions are always '=' followed by 3 characters, so they should be easiest to identify and cut.
        j = ''
        c = ''
        d = ''
        EQ = asmlist[i].find('=')
        
        
        if asmlist[i][ilength-4] == ';':
            j = asmlist[i][(ilength-3):ilength]
            #print('Jump')
            print(j)
            if EQ != -1:
                d = asmlist[i][0:EQ]
                c = asmlist[i][(EQ+1):(ilength-4)]
                print(c)
                #print(d)
            else:
                d = ''
                c = asmlist[i][0:ilength-4]
                print(c)
                #print(d)

        #Next: Data is only saved if there is an = sign. If there is an equal sign, it can be preset.
        else:
            if EQ != -1:
                d = asmlist[i][0:EQ]
                c = asmlist[i][(EQ+1):ilength]
                #print(c)
                #print(d)
            else:
                d = ''
                c = asmlist[i][0:ilength]
                #print(c)
                #print(d)
        
        binlist.append(C_constructor(c,d,j))
        #print(C_constructor(c,d,j))

        

        
        
binfile = '\n'.join(binlist)        

#print('\n\n')
#print(binfile)
#print('\n\n')

#For comparison purposes, this prints a numbered list of binary instructions to the console.
binlist2 =[]
for i in range(0,len(binlist)):
    binlist2.append( f'{i}. ' + binlist[i])

print('\n'.join(binlist2))

with open("project_6/bin/"+ fname+ ".hack", "w") as f:
  f.write(binfile)



#Instruction parser

#Strip away any leading spaces.
#Based on first character, classify as location, A-instruction or C-instruction.
#For loop [Check how those are realized] (
#For A-instruction, differentiate between straight and named (Named ones are also jump locations, or input devices?)
##For straight A instructions, interpretation should be easy.
##For others, interpretation may require some extra work.
#For C-instructions, seperate them into their three parts using = and ,
#...as seperators. Then recombine based on the composition table

#I need to define the preset addresses such as screen and maybe addr in the program itself.
#A can remain as 0 if neither A nor M are inputs. 




















    
        






    


