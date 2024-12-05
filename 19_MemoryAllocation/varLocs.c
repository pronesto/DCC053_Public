#include <stdio.h>
#include <stdlib.h>

// Static memory: Global and static variables are allocated here
int global_var = 10; // Global variable (static memory)

void allocateMemory() {
    // Stack memory: Local variables in functions are allocated here
    int local_var = 20; // Local variable (stack memory)

    // Heap memory: Dynamically allocated memory
    int* heap_var = (int*) malloc(sizeof(int)); // Allocated on the heap
    *heap_var = 30;

    // Print memory locations
    printf("Address of global_var (static memory): %p\n", (void*)&global_var);
    printf("Address of local_var (stack memory): %p\n", (void*)&local_var);
    printf("Address of heap_var (heap memory): %p\n", (void*)heap_var);

    // Free dynamically allocated memory
    free(heap_var);
}

int main() {
    allocateMemory();
    return 0;
}

