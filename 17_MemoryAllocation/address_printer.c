#include <stdio.h>
#include <stdlib.h>

// Global variable (BSS section, uninitialized)
int g_uninitialized;

// Global variable (Data section, initialized)
int g_initialized = 42;

int main() {
    // Local variable (Stack section)
    int local_var = 100;

    // Dynamically allocated memory (Heap section)
    int *heap_var = (int*)malloc(sizeof(int));

    // Printing addresses from different memory segments
    printf("main (Text segment, code): %p\n", (void*)main);
    printf("g_initialized (Data segment): %p\n", (void*)&g_initialized);
    printf("g_uninitialized (BSS segment): %p\n", (void*)&g_uninitialized);
    printf("local_var (Stack): %p\n", (void*)&local_var);
    printf("heap_var (Heap): %p\n", (void*)heap_var);

    // Free the heap memory
    free(heap_var);

    return 0;
}

