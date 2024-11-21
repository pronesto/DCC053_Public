#include <stdio.h>
#include <stdint.h>
#include <stddef.h>

#define HEAP_SIZE 1024  // Total size of the simulated heap.
#define ALIGNMENT 8     // Memory alignment (for performance and portability).

// Align `size` to the nearest multiple of `ALIGNMENT`.
#define ALIGN(size) (((size) + (ALIGNMENT - 1)) & ~(ALIGNMENT - 1))

// Metadata for each memory block.
typedef struct BlockHeader {
    size_t size;            // Size of the block (excluding header).
    int is_free;            // Whether the block is free.
    struct BlockHeader* next; // Pointer to the next block (linked list).
} BlockHeader;

// The heap memory pool.
static uint8_t heap[HEAP_SIZE];

// Pointer to the start of the free list.
static BlockHeader* free_list = NULL;

// Initialize the heap.
void init_heap() {
    free_list = (BlockHeader*)heap;
    free_list->size = HEAP_SIZE - sizeof(BlockHeader);
    free_list->is_free = 1;
    free_list->next = NULL;
}

// malloc implementation.
void* my_malloc(size_t size) {
    if (size == 0) {
        return NULL;
    }

    size = ALIGN(size); // Align the requested size.
    BlockHeader* current = free_list;

    while (current) {
        if (current->is_free && current->size >= size) {
            // Found a suitable block.
            size_t remaining = current->size - size;
            if (remaining > sizeof(BlockHeader)) {
                // Split the block if there's enough space left.
                BlockHeader* new_block = (BlockHeader*)((uint8_t*)current + sizeof(BlockHeader) + size);
                new_block->size = remaining - sizeof(BlockHeader);
                new_block->is_free = 1;
                new_block->next = current->next;

                current->next = new_block;
                current->size = size;
            }

            current->is_free = 0; // Mark the block as allocated.
            return (void*)((uint8_t*)current + sizeof(BlockHeader));
        }

        current = current->next;
    }

    // No suitable block found.
    return NULL;
}

// free implementation.
void my_free(void* ptr) {
    if (!ptr) {
        return;
    }

    BlockHeader* block = (BlockHeader*)((uint8_t*)ptr - sizeof(BlockHeader));
    block->is_free = 1;
}

// Debug function to print the heap state.
void print_heap() {
    BlockHeader* current = free_list;
    printf("Heap state:\n");
    while (current) {
        printf("Block at %p: size=%zu, is_free=%d\n", (void*)current, current->size, current->is_free);
        current = current->next;
    }
}

int main() {
    init_heap();

    void* a = my_malloc(100);
    void* b = my_malloc(200);
    print_heap();

    my_free(a);
    print_heap();

    void* c = my_malloc(50);
    print_heap();

    return 0;
}

