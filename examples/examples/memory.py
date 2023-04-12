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
    try: #error handling
        input_file = arg[1]
        print(input_file)

    except: #if error happens
        print("error")



def myalloc(size):
    """
    takes an integer value indicating the number of bytes to allocate for the pyload of the block
    returns a pointer to the starting address of the pyload of the allocated bloack
    """
    pass


def myrealloc(pointer, size):
    """
    takes a pointer to an allocated block and an integer value to resize the bloack to 
    returns a pointer to the new block
    copies the payload from the old block tot he new block
    frees the old block
    a call to myrealloc with a size of zero is equivalent to a call to my free
    """
    pass


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




if __name__ == "__main__":
    main(sys.argv)
