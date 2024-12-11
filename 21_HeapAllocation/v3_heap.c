#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define HEAP_SIZE 64 // Total size of the simulated heap.

static uint8_t heap[HEAP_SIZE]; // The heap memory pool.

// Metadata for each memory block.
typedef struct BlockHeader {
  uint8_t size;      // Size of the block (excluding header).
  uint8_t is_free;   // Whether the block is free (1 = free, 0 = allocated).
  uint8_t next;      //  Offset to the next block in the heap (0 if none).
  uint8_t ref_count; // Reference counter for garbage collection.
} BlockHeader;

// Pointer (offset) to the start of the free list.
static uint8_t free_list = 0; // Start at the beginning of the heap.

// Initialize the heap by setting up a single large free block.
void init_heap() {
  BlockHeader *initial = (BlockHeader *)heap;
  initial->size = HEAP_SIZE - sizeof(BlockHeader);
  initial->is_free = 1;
  initial->next = 0;      // End of the list.
  initial->ref_count = 0; // Initialize reference count to 0.
}

// malloc implementation.
void *my_malloc(uint8_t size) {
  uint8_t current_offset = free_list;

  while (current_offset < HEAP_SIZE) {
    BlockHeader *current = (BlockHeader *)&heap[current_offset];

    // Check if the current block is free and large enough to accommodate the
    // requested size.
    if (current->is_free && current->size >= size) {

      uint8_t remaining = current->size - size;

      if (remaining > sizeof(BlockHeader)) {
        // Split the block if the remaining space is enough to hold another
        // block.
        uint8_t new_offset = current_offset + sizeof(BlockHeader) + size;
        BlockHeader *new_block = (BlockHeader *)&heap[new_offset];
        new_block->size =
            remaining - sizeof(BlockHeader); // Update size of the new block.
        new_block->is_free = 1;              // Mark the new block as free.
        new_block->ref_count = 0; // initialize reference counting as 0.
        new_block->next =
            current->next; // Link the new block to the rest of the list.

        current->next = new_offset;
        current->size = size;
      }

      current->is_free = 0;   // Mark the block as allocated.
      current->ref_count = 1; // Initialize reference count to 1.
      return &heap[current_offset + sizeof(BlockHeader)];
    }

    current_offset = current->next;
    if (current_offset == 0) {
      break; // Reached the end of the list.
    }
  }

  // No suitable block found.
  return NULL;
}

// Custom free implementation to release allocated memory back to the heap.
void my_free(void *ptr) {
  if (!ptr)
    return; // Ignore NULL pointers.

  // Calculate the offset of the block being freed.
  uint8_t block_offset = (uint8_t *)ptr - heap - sizeof(BlockHeader);
  BlockHeader *block = (BlockHeader *)&heap[block_offset];

  if (!block->is_free) {
    block->is_free = 1; // Mark the block as free.

    // Attempt to coalesce with the next block.
    if (block->next != 0) {
      BlockHeader *next_block = (BlockHeader *)&heap[block->next];
      if (next_block->is_free) {
        block->size += sizeof(BlockHeader) + next_block->size;
        block->next = next_block->next;
      }
    }
  }
}

// Increment the reference count of a block.
void increment_ref(void *ptr) {
  if (!ptr)
    return;

  uint8_t block_offset = (uint8_t *)ptr - heap - sizeof(BlockHeader);
  BlockHeader *block = (BlockHeader *)&heap[block_offset];
  block->ref_count++;
}

// Decrement the reference count of a block and free it if the count reaches 0.
void decrement_ref(void *ptr) {
  if (!ptr)
    return;

  uint8_t block_offset = (uint8_t *)ptr - heap - sizeof(BlockHeader);
  BlockHeader *block = (BlockHeader *)&heap[block_offset];

  if (block->ref_count > 0) {
    block->ref_count--;

    if (block->ref_count == 0) {
      my_free(ptr); // Free the block when the reference count reaches 0.
    }
  }
}

// Debugging function to display the heap structure.
void print_heap() {
  uint8_t current_offset = free_list; // Start from the free list pointer.

  printf("Heap layout:\n");
  while (current_offset < HEAP_SIZE) {
    BlockHeader *current = (BlockHeader *)&heap[current_offset];
    printf("Offset: %d, Size: %d, Free: %d, RefCount: %d, Next: %d\n",
           current_offset, current->size, current->is_free, current->ref_count,
           current->next);
    current_offset = current->next; // Move to the next block in the list.
    if (current_offset == 0)
      break; // End of the list.
  }
  printf("\n");
}

// Debug function to print the heap state.
void dump() {
  printf("Heap State:\n");
  for (int i = 0; i < HEAP_SIZE; i += 8) { // Print 8 bytes per line.
    for (int j = i; j < i + 8; ++j) {
      printf("%4d: %4d, ", j, heap[j]);
    }
    printf("\n");
  }
}

// Example usage.
int main() {
  init_heap();
  void *a = my_malloc(20);
  dump();
  {
    void *b = a; // Increment the reference count.
    increment_ref(b);
    dump();

    void *c = my_malloc(10); // Allocate another block.
    dump();

    decrement_ref(c); // Decrement and free block c.
    decrement_ref(b); // Now block a is freed.
  }
  dump();

  decrement_ref(a); // Decrement but still referenced by b.
  dump();
  return 0;
}
