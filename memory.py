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





def main(arg):
    global pointer_dict, virMem
    input_file = ""
    try: #error handling
        input_file = arg[1]
        print(input_file)
    except: #if error happens
        print("error")
    virMem = [None] *1000
    pointer_dict = {} 
    virMem[0],virMem[1],virMem[998],virMem[999] = 1,3992,3992,1
    #with open("examples/examples/" + input_file, "r") as f:
    with open(input_file, "r") as f:
        for line in f:
            print(line)
            oper = line.split(",")
            print(oper)
            if oper[0] == "a":
                pointer_dict[int(oper[2].strip().strip('\n'))] = myalloc(int(oper[1]))
            elif oper[0] == "f":
                myfree(pointer_dict[int(oper[1].strip().strip('\n'))])
                pointer_dict.pop(int(oper[1]))
            elif oper[0] == "r":
                pointer_dict[int(oper[3].strip().strip('\n'))] = myrealloc(pointer_dict[int(oper[2])],int(oper[1]))
                myfree(pointer_dict[int(oper[2])])
                pointer_dict.pop(int(oper[2]))


    print(pointer_dict)
    print_result(virMem)
    

def myalloc(size):
    """
    takes an integer value indicating the number of bytes to allocate for the pyload of the block
    returns a pointer to the starting address of the pyload of the allocated bloack
    """
    n = 1
    free_size = 0
    while(True):
        print(n)
        print(virMem[n])
        if virMem[n] & 1 == 0 and virMem[n] >= 8 + (((size//8) + 1) * 8):
            break
        else:
            n = n + (virMem[n] - 1) // 4
    free_size = virMem[n]
    size_block =  (((size//8) + 1)*8) + 8 + 1
    virMem[n] = size_block
    virMem[n + ((size_block - 1)//4) - 1] = size_block
    virMem[n + ((size_block - 1)//4) ] = free_size - (size_block - 1)
    virMem[n + free_size//4 - 1]  = free_size - (size_block - 1)
    return n

def myrealloc(pointer, size):
    """
    takes a pointer to an allocated block and an integer value to resize the bloack to 
    returns a pointer to the new block
    copies the payload from the old block tot he new block
    frees the old block
    a call to myrealloc with a size of zero is equivalent to a call to my free
    """
    n = 1
    free_size = 0
    while(True):
        print(n)
        print(virMem[n])
        if virMem[n] & 1 == 0 and virMem[n] >= 8 + (((size//8) + 1) * 8):
            break
        elif virMem[n] & 1 == 0 and virMem[n] < 8 + (((size//8) + 1) * 8):
            n = n + virMem[n]//4
        else:
            n = n + (virMem[n] - 1) // 4
    free_size = virMem[n]
    size_block =  (((size//8) + 1)*8) + 8 + 1
    virMem[n] = size_block
    virMem[n + ((size_block - 1)//4) - 1] = size_block
    virMem[n + ((size_block - 1)//4) ] = free_size - (size_block - 1)
    virMem[n + free_size//4 - 1]  = free_size - (size_block - 1)

    for old_block in range((virMem[pointer]-9)//4):
        virMem[n + 1 + old_block] = virMem[pointer + 1 + old_block]


    return n


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
    free_amount = 0

    if virMem[pointer - 1] & 1 == 0 and virMem[pointer + (virMem[pointer]-1)//4] & 1 == 0: #free and free
        free_amount = virMem[pointer - 1]
        free_amount = free_amount + virMem[pointer] -1
        virMem[pointer - (virMem[pointer -1]//4)] = free_amount
        virMem[pointer - (virMem[pointer-1]//4) + (free_amount//4) -1] = free_amount

        pointer = pointer - (virMem[pointer -1]//4)

        free_amount = virMem[pointer + (virMem[pointer]-1)//4]
        free_amount = free_amount + virMem[pointer] - 1
        virMem[pointer] = free_amount
        virMem[pointer + (free_amount//4) - 1] = free_amount

    elif virMem[pointer - 1] & 1 == 0 and virMem[pointer + (virMem[pointer]-1)//4] & 1 == 1: #free and alloced
        free_amount = virMem[pointer - 1]
        free_amount = free_amount + virMem[pointer] -1
        virMem[pointer - (virMem[pointer -1]//4)] = free_amount
        virMem[pointer - (virMem[pointer-1]//4) + (free_amount//4) -1] = free_amount

    elif virMem[pointer - 1] & 1 == 1 and virMem[pointer + (virMem[pointer]-1)//4] & 1 == 0: #alloced and free
        free_amount = virMem[pointer + (virMem[pointer]-1)//4]
        free_amount = free_amount + virMem[pointer] - 1
        virMem[pointer] = free_amount
        virMem[pointer + (free_amount//4) - 1] = free_amount

    else:# alloced and alloced
        virMem[pointer] = virMem[pointer]-1
        virMem[pointer + (virMem[pointer])//4 - 1] = virMem[pointer]

    pass

def mysbrk(size):
    """
    grows or shrinks the size of the heap by a number of words specified by the input parameter size
    you may call this whenever you need to in the course of a simulation, as you need to grow the heap
    -> only as much as needed for the allocation, do no extend a free block at the end of the previous space,
    -> use a totally new block.
    thsi call will return an error and halt the simulation if your heap would need to grow past the maximum
    -> size of 100,000 words.
    """
    pass

def print_result(memory):
    for block_num in range(len(memory)):
        if memory[block_num] == None:
            print("{}, {}".format(block_num, " "))
        else: 
            print("{}, 0x{:08X}".format(block_num, memory[block_num]))
    


if __name__ == "__main__":
    main(sys.argv)
