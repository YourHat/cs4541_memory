###########################################
#       CS4541
#       Memory Allocation Simulator
#       Yutaroh Tanaka
#       Yutaroh.Tanaka@wmich.edu
###########################################
"""
start your heap at address 0
32 bit system - each word with 4 bytes 
initial heap will be 1000 words
"""
import sys # to get argv
import time




def main(arg):
    global pointer_dict, virMem, imp_exp, fir_bes
    input_file = ""
    try: #error handling
        imp_exp = arg[1] #implicit or explicit
        fir_bes = arg[2] # first of best 
        input_file = arg[3] # file name
        print(input_file)
    except: #if error happens
        print("error")


    virMem = [None] *1000 #initialize virtual memory
    pointer_dict = {} # {ptr:adress of the ptr}
    virMem[0],virMem[1],virMem[998],virMem[999] = 1,3992,3992,1 #initialze virtual memrory
    #with open("examples/examples/" + input_file, "r") as f:
    with open(input_file, "r") as f:
        for line in f: #read every line
            print(line)
            oper = line.split(",") #split with ","
            print(oper)
            if oper[0] == "a": # if alloc
                if len(virMem) + ((int(oper[1])//8) + 1) * 2 < 100000: # make sure its less than 100,000 words
                    pointer_dict[int(oper[2].strip().strip('\n'))] = myalloc(int(oper[1])) # call myalloc and add an item in dict
            elif oper[0] == "f": # if free
                myfree(pointer_dict[int(oper[1].strip().strip('\n'))]) # call myfree 
                pointer_dict.pop(int(oper[1])) # get rid of an item from dict
            elif oper[0] == "r": # if realloc
                if len(virMem) + ((int(oper[1])//8) + 1) * 2 < 100000: # make sure its less than 100,000 words
                    pointer_dict[int(oper[3].strip().strip('\n'))] = myrealloc(pointer_dict[int(oper[2])],int(oper[1])) # call myrealloc and add an item in dict
                    myfree(pointer_dict[int(oper[2])]) # call myfree for the original address
                    pointer_dict.pop(int(oper[2])) # get rid of an item (original address) form dict 
 
    print(pointer_dict)
    print_result(virMem) # call print_result to print virtual memory
    

def myalloc(size):
    """
    takes an integer value indicating the number of bytes to allocate for the pyload of the block
    returns a pointer to the starting address of the pyload of the allocated bloack
    """
    n = 1 # starting memory address
    free_size = 0 # free_size 
    size_needed = 0 # memory size with header and footer
    if size%8 != 0: #if the size cannot be devided by 8, add extra 8 bytes (two blocks)
        size_needed = 8 
    size_needed = size_needed + (((size//8)*8) +8) # overall size needed to alloc
    found = False # it is for best-fit
    if(fir_bes) == "f": # if its first fit
        while(True):
            if n != len(virMem) -1: # if you reach to the end of the VM, call mysbrk
                if virMem[n] & 1 == 0 and virMem[n] >= size_needed: # if there is a free memory with enough size
                   break
                elif virMem[n] & 1 == 0 and virMem[n] <size_needed: # if there is a free memory but not enough size
                    n = n + virMem[n]//4 # go to the next block
                else: # if its not free
                    n = n + (virMem[n] - 1) // 4 #go to the next block
            else:
                mysbrk(size) #call mysbrk
    else: # best fit
        best_list = [] # list of free block that has enough size for the memroy allcation
        while(True):
            if n != len(virMem)-1:# if you reach to the end of the VM, call mysbrk
                if virMem[n] & 1 == 0 and virMem[n] == size_needed: # if there is a free memory with the same size
                    break
                elif virMem[n] & 1 == 0 and virMem[n] > size_needed: #if there is a free memory but more than enough size
                    best_list.append([virMem[n], n]) # add the address and size tot the list
                    found = True 
                    n = n + virMem[n]//4 # go to the next block
                elif virMem[n] & 1 == 0 and virMem[n] <size_needed: # if there is a free memory but not big enough
                    n = n + virMem[n]//4 # go to the next block
                else: # if its not free
                    n = n + (virMem[n] - 1) // 4 # go to the next block
            else: # if there is no free block with the same size
                if found: # if there is a block with more than enough size
                    smallest = best_list[0] # set the smallest block to the first item in the list
                    for i in best_list: # go though the list
                        if smallest[0] >= i[0]: #if the size is smaller than the current smallest one 
                            smallest = i #set the item as the smallest block
                    n = smallest[1] # set the address 
                    break
                mysbrk(size) # if there is no memory with enough size
                
    free_size = virMem[n] # for the free block right after
    size_block = 0 # initialize the size of block needed
    if size%8 != 0:
        size_block = 8
    size_block = size_block + (((size//8))*8) + 8 + 1
    virMem[n] = size_block # change the header
    virMem[n + ((size_block - 1)//4) - 1] = size_block # change the footer
    if (n + ((size_block - 1)//4)) != len(virMem) -1: # if the next block is not the last block
        if virMem[n + ((size_block - 1)//4)] == None: # if the next block is None
            virMem[n + ((size_block - 1)//4) ] = free_size - (size_block - 1)
            virMem[n + free_size//4 - 1]  = free_size - (size_block - 1)
        elif virMem[n + ((size_block - 1)//4)] & 1 == 0: # if the next block is free block
            virMem[n + ((size_block - 1)//4) ] = free_size - (size_block - 1)
            virMem[n + free_size//4 - 1]  = free_size - (size_block - 1)
    
    return n # return the address of the block


def myrealloc(pointer, size):
    """
    takes a pointer to an allocated block and an integer value to resize the bloack to 
    returns a pointer to the new block
    copies the payload from the old block tot he new block
    frees the old block
    a call to myrealloc with a size of zero is equivalent to a call to my free
    """
    n = 1 # starting memory address
    free_size = 0 # free_size 
    size_needed = 0 # memory size with header and footer
    if size%8 != 0: #if the size cannot be devided by 8, add extra 8 bytes (two blocks)
        size_needed = 8 
    size_needed = size_needed + (((size//8)*8) +8) # overall size needed to alloc
    found = False # it is for best-fit
    if(fir_bes) == "f": # if its first fit
        while(True):
            if n != len(virMem) -1: # if you reach to the end of the VM, call mysbrk
                if virMem[n] & 1 == 0 and virMem[n] >= size_needed: # if there is a free memory with enough size
                   break
                elif virMem[n] & 1 == 0 and virMem[n] <size_needed: # if there is a free memory but not enough size
                    n = n + virMem[n]//4 # go to the next block
                else: # if its not free
                    n = n + (virMem[n] - 1) // 4 #go to the next block
            else:
                mysbrk(size) #call mysbrk
    else: # best fit
        best_list = [] # list of free block that has enough size for the memroy allcation
        while(True):
            if n != len(virMem)-1:# if you reach to the end of the VM, call mysbrk
                if virMem[n] & 1 == 0 and virMem[n] == size_needed: # if there is a free memory with the same size
                    break
                elif virMem[n] & 1 == 0 and virMem[n] > size_needed: #if there is a free memory but more than enough size
                    best_list.append([virMem[n], n]) # add the address and size tot the list
                    found = True 
                    n = n + virMem[n]//4 # go to the next block
                elif virMem[n] & 1 == 0 and virMem[n] <size_needed: # if there is a free memory but not big enough
                    n = n + virMem[n]//4 # go to the next block
                else: # if its not free
                    n = n + (virMem[n] - 1) // 4 # go to the next block
            else: # if there is no free block with the same size
                if found: # if there is a block with more than enough size
                    smallest = best_list[0] # set the smallest block to the first item in the list
                    for i in best_list: # go though the list
                        if smallest[0] >= i[0]: #if the size is smaller than the current smallest one 
                            smallest = i #set the item as the smallest block
                    n = smallest[1] # set the address 
                    break
                mysbrk(size) # if there is no memory with enough size


    free_size = virMem[n] # for the free block right after
    size_block = 0 # initialize the size of block needed
    if size%8 != 0:
        size_block = 8
    size_block = size_block + (((size//8))*8) + 8 + 1
    virMem[n] = size_block # change the header
    virMem[n + ((size_block - 1)//4) - 1] = size_block # change the footer
    if (n + ((size_block - 1)//4)) != len(virMem) -1: # if the next block is not the last block
        if virMem[n + ((size_block - 1)//4)] == None: # if the next block is None
            virMem[n + ((size_block - 1)//4) ] = free_size - (size_block - 1)
            virMem[n + free_size//4 - 1]  = free_size - (size_block - 1)
        elif virMem[n + ((size_block - 1)//4)] & 1 == 0: # if the next block is free block
            virMem[n + ((size_block - 1)//4) ] = free_size - (size_block - 1)
            virMem[n + free_size//4 - 1]  = free_size - (size_block - 1)

    for old_block in range((virMem[pointer]-9)//4): #copy form the original block
        virMem[n + 1 + old_block] = virMem[pointer + 1 + old_block]

    return n # return address of the block


def myfree(pointer):
    """
    must use LIFO policy for explicit free lists
    prev pointer should be first and next pointer should ve second
    frees the block pointed to by the input parameter pointer
    returns nothing
    only works if pointer represents a previously allocated or reallocated block that has not yet been freed
    otherwise, does not change the heap
    coalesce after freeing. coalesce lower before coalescing higher address, and update headers last
    """

    free_amount = 0 # amount being freed

    if virMem[pointer - 1] & 1 == 0 and virMem[pointer + (virMem[pointer]-1)//4] & 1 == 0: #free and free
        free_amount = virMem[pointer - 1] # size of memory freed
        free_amount = free_amount + virMem[pointer] -1 # add the free memory prev
        free_amount = free_amount + virMem[pointer + (virMem[pointer]-1)//4] # add the free memory next
        
        virMem[pointer - (virMem[pointer - 1]//4)] = free_amount # change the size of free memory for header
        virMem[pointer - (virMem[pointer - 1]//4) -1 + (free_amount//4)] = free_amount #change the size of free memroy for footer


    elif virMem[pointer - 1] & 1 == 0 and virMem[pointer + (virMem[pointer]-1)//4] & 1 == 1: #free and alloced
        free_amount = virMem[pointer - 1] # size of memory freed
        free_amount = free_amount + virMem[pointer] -1 # add the free memory prev
        virMem[pointer - (virMem[pointer -1]//4)] = free_amount #change the size of free memory for header
        virMem[pointer - (virMem[pointer-1]//4) + (free_amount//4) -1] = free_amount #change the size of free memory for footer

    elif virMem[pointer - 1] & 1 == 1 and virMem[pointer + (virMem[pointer]-1)//4] & 1 == 0: #alloced and free
        free_amount = virMem[pointer + (virMem[pointer]-1)//4] # size of next free memory
        free_amount = free_amount + virMem[pointer] - 1 #add the freed memory amount
        virMem[pointer] = free_amount #change the size of free memory for header
        virMem[pointer + (free_amount//4) - 1] = free_amount #change the size of free memory for footer

    else:# alloced and alloced
        virMem[pointer] = virMem[pointer]-1 # size of memory freed and change the header
        virMem[pointer + (virMem[pointer])//4 - 1] = virMem[pointer] # change the footer


def mysbrk(size):
    """
    grows or shrinks the size of the heap by a number of words specified by the input parameter size
    you may call thi
    -> only as much as needed for the allocation, do no extend a free block at the end of the previous space,
    -> use a totally new block.
    thsi call will return an error and halt the simulation if your heap would need to grow past the maximum
    -> size of 100,000 words.
    """
    expand_size = 0
    if size%8 != 0: # if size cannot be devided by 8
        expand_size = 8 #add extra 8
    expand_size = expand_size + (size//8)*8 + 8 #size needed to be expanded
    virMem[-1] = expand_size #change the last virtual memory before expand the memory size -> header
    for i in range((expand_size//4)): #expand the memory
        virMem.append(None)
    virMem[-2] = expand_size #change the 2nd to the last itme of the virtual memory -> footer
    virMem[-1] = 1 #change the last item of the vm to 1

    

def print_result(memory):
    """
    print the result
    """
    for block_num in range(len(memory)): #go though all the item in vm
        if memory[block_num] == None: #if None -> print address, but not the value
            print("{}, {}".format(block_num, " "))
        else: #if there is a vaule, print adddres and value
            print("{}, 0x{:08X}".format(block_num, memory[block_num])) #format the vlue to the hex
    


if __name__ == "__main__": # call the main function
    main(sys.argv)
