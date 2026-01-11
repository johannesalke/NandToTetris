#Final checks: find and replace 'asmlist' > 'vmlist'
import sys

fname = ''
if __name__ == "__main__":
    fname = sys.argv[1]

#0. Defining functions


#This function determines the push/pop target address for the first four segments.
#It saves the resulting address to R13        
def paddress(seg,x):
    res = '' + '@'
    
    
    print(res)
    return res


def pother(action, segment, value):
    res = '' 
    act = ''
    if segment == 'local':
        act = act + 'LCL, '
    elif segment == 'argument':
        act = act + 'ARG, '
    elif segment == 'this':
        act = act + 'THIS, '
    elif segment == 'that':
        act = act + 'THAT, '
        
    if action =='pop':
        res = res + '@' + act + 'D=M, @'+str(value)+', D=D+A, @R13, M=D, '
        res = res + '@SP, M=M-1, A=M, D=M, @R13, A=M, M=D, '



    elif action =='push':
        res = res + '@' + act + 'D=M, @'+str(value)+', A=D+A, D=M, '

        res = res + '@SP, A=M, M=D, @SP, M=M+1, '
    return res
    



#Pusing constants. Finished, untested.
def pushconst(const):
    res = '@' + str(const) + ',D=A, @SP, A=M, M=D, @SP, M=M+1, '
    #print(res)
    return res


#Operations using static files.
def pstatic(action, value):
    symbol = '@' + fname + '.' + str(value) + ', '
    res = ''
    #Pop assignes static variables.
    if action == 'pop':
        res = res + '@SP, M=M-1, A=M, D=M, ' + symbol + 'M=D, '
        

    #Push writes static variables to the stack.
    else:
        res = res + symbol + 'D=M, @SP, A=M, M=D, @SP, M=M+1, '

    #print(res)
    return(res)

    

    

#Entire Pointer translation. Finished, untested
def ppointer(action,value):
    res = ''
    if action == 'push':
        if value == '0':         
            res = res + '@THIS, D=M, @SP, A=M, M=D, @SP, M=M+1, '
        else:
            res = res + '@THAT, D=M, @SP, A=M, M=D, @SP, M=M+1, '

    elif action == 'pop':
        res = res + '@SP, M=M-1, A=M, D=M, '
        if value == '0':
            res = res + '@THIS, M=D, '
        else:
            res = res + '@THAT, M=D, '

    #print(res)
    return(res)


def ptemp(action,value):    
    res = ''
    if action == 'pop':    
        res = res + '@SP, M=M-1, A=M, D=M, ' +  '@R'+str(int(value)+5)+', M=D, '

    elif action == 'push':
        
        res = res + '@R'+str(int(value)+5)+', D=M, @SP, A=M, M=D, @SP, M=M+1, '


    return res





#1. Ask which VM code file should be translated.

fname = input()


#2. Read in the file.
with open("project_7/"+ fname+ ".vm", "r") as assembly:
    asm = assembly.read()
    vmlist = asm.splitlines()
    #print(vmlist)


#3.1: Remove empty strings
vmlist = [x for x in vmlist if x.strip()]

list2 = []
for i in vmlist:   
    list2.append(i.strip())

vmlist = list2

#print(vmlist)

#3.2: Remove comments
vmlist = [ x for x in vmlist if "/" not in x ]

    
#Check that comments and blank lines have been properly removed.
print(vmlist)




#4. Setting up the initial instructions and the relevant pointers
asmlist = []

SP_init = ' @256, D=A, @SP, M=D, '
LCL_init = '@20, D=A, @LCL, M=D, '
ARG_init = '@30, D=A, @ARG, M=D, '
THIS_init = '@40, D=A, @THIS, M=D, '
THAT_init = '@50, D=A, @THAT, M=D, '

asmlist.append(SP_init)
asmlist.append(LCL_init)
asmlist.append(ARG_init)
asmlist.append(THIS_init)
asmlist.append(THAT_init)

    


#?: Seperate by instruction type and translate each.
for i in range(0,len(vmlist)):
    ilength = len(vmlist[i])

    if vmlist[i][0] == 'p':
        pinstr = vmlist[i]
        #Splitting push/pop instructions into 3 parts: Action, segment, value
        pinstr = pinstr.split()
        paction = pinstr[0]
        psegment = pinstr[1]
        pvalue = pinstr[2]

        if psegment =='constant':
            asmlist.append(pushconst(pvalue))

        elif psegment == 'static':
            asmlist.append(pstatic(paction,pvalue))

        elif psegment == 'pointer':
            asmlist.append(ppointer(paction,pvalue))

        elif psegment == 'temp':
            asmlist.append(ptemp(paction,pvalue))

        else:
            asmlist.append(pother(paction, psegment, pvalue))
        
        


    #arithmetic
    elif vmlist[i] == 'add':
        #res = '@SP, M=M-1, A=M, D=M, @SP, M=M-1, A=M, D=D+M, @SP, A=M, M=D, @SP, M=M+1, '
        res = '@SP, M=M-1, A=M, D=M, A=A-1, M=D+M, '
        print(res)
        asmlist.append(res)

        
    elif vmlist[i] == 'sub':
        #res = '@SP, M=M-1, A=M, D=M, @SP, M=M-1, A=M, D=D-M, D=-D, @SP, A=M, M=D, @SP, M=M+1, '
        res = '@SP, M=M-1, A=M, D=M, @SP, M=M-1, A=M, M=M-D, @SP, M=M+1, '
        print(res)
        asmlist.append(res) 
    elif vmlist[i] == 'neg':
        res = '@SP, A=M, A=A-1 M=-M, '
        print(res)
        asmlist.append(res)
        
    #Comparisons
    elif vmlist[i] == 'eq':
        label = '(comp' + str(i) +')'
        
        asmlist.append(f'@SP, M=M-1, A=M, D=M, @SP, M=M-1, A=M, D=M-D, @comp{i}a, D;JEQ, @0, D=A, @SP, A=M, M=D, @comp{i}b, 0;JMP, (comp{i}a), @1, A=-A, D=A, @SP, A=M, M=D, (comp{i}b), @SP, M=M+1, ')
        
    elif vmlist[i] == 'gt':
        asmlist.append(f'@SP, M=M-1, A=M, D=M, @SP, M=M-1, A=M, D=M-D, @comp{i}a, D;JGT, @0, D=A, @SP, A=M, M=D, @comp{i}b, 0;JMP, (comp{i}a), @1, A=-A, D=A, @SP, A=M, M=D, (comp{i}b), @SP, M=M+1, ')
        
    elif vmlist[i] == 'lt':
        asmlist.append(f'@SP, M=M-1, A=M, D=M, @SP, M=M-1, A=M, D=M-D, @comp{i}a, D;JLT, @0, D=A, @SP, A=M, M=D, @comp{i}b, 0;JMP, (comp{i}a), @1, A=-A, D=A, @SP, A=M, M=D, (comp{i}b), @SP, M=M+1, ')
        
    #Boolean
    elif vmlist[i] == 'and':
        res = '@SP, M=M-1, A=M, D=M, A=A-1, M=D&M, '
        print(res)
        asmlist.append(res)
        
    elif vmlist[i] == 'or':
        res = '@SP, M=M-1, A=M, D=M, A=A-1, M=D|M, '
        print(res)
        asmlist.append(res)
    elif vmlist[i] == 'not':
        res = '@SP, A=M, A=A-1, M=!M, '
        print(res)
        asmlist.append(res)
    #Not closing with an if to leave space for the next commands.
    











#Final: Replace Commas and write to file.
#asmlist2 = []
#for x in asmlist:
#    x.replace(',','\n')
#    asmlist2.append(x)
    
#asmlist = asmlist2
    

asmfile = ''.join(asmlist)
asmfile = asmfile.replace(',','\n')

#print('\n\n')

#print(asmfile)

print('\n\n')

#binlist2 =[]
#for i in range(0,len(binlist)):
#    binlist2.append( f'{i}. ' + binlist[i])

#print('\n'.join(binlist2))

with open("project_7/asm/"+ fname+ ".asm", "w") as f:
  f.write(asmfile)



















#Increment pointer: @SP, M=M+1
#Decrement pointer: @SP, M=M-1











#Memory Segmentation
#Total non-I/O memory locations: 16384
#Locations per segment: 2048
#segments = [local, argument, this, that, constant, static, pointer, temp]


#!This doesn't include the stack yet! Or the program variables!
#Well, the stack pointer is probably located in pointer...

#The constant segment can be replaced with just using @i instead. 









