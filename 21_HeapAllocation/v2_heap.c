#include <stdint.h>
#include <stdio.h>

#define HEAP_SIZE 128 // Total size of the simulated heap.

static uint8_t heap[HEAP_SIZE]; // The heap memory pool.

// Metadata for each memory block.
typedef struct BlockHeader {
  uint8_t size;    // Size of the block (excluding header).
  uint8_t is_free; // Whether the block is free (1 = free, 0 = allocated).
  uint8_t next;    //  Offset to the next block in the heap (0 if none).
} BlockHeader;

// Pointer (offset) to the start of the free list.
static uint8_t free_list = 0; // Start at the beginning of the heap.

// Initialize the heap by setting up a single large free block.
void init_heap() {
  BlockHeader *initial = (BlockHeader *)heap;
  initial->size = HEAP_SIZE - sizeof(BlockHeader);
  initial->is_free = 1; // Mark the block as free.
  initial->next = 0;    // No other blocks in the list initially.
}

//  Custom malloc implementation to allocate memory from the heap.
void *my_malloc(uint8_t size) {
  uint8_t current_offset = free_list; // Start from the free list pointer.

  while (current_offset < HEAP_SIZE) {
    BlockHeader *current = (BlockHeader *)&heap[current_offset];

    // Check if the current block is free and large enough to accommodate the
    // requested size.
    if (current->is_free && current->size >= size) {
      uint8_t remaining =
          current->size - size; // Calculate remaining space after allocation.

      if (remaining > sizeof(BlockHeader)) {
        // Split the block if the remaining space is enough to hold another
        // block.
        uint8_t new_offset = current_offset + sizeof(BlockHeader) + size;
        BlockHeader *new_block = (BlockHeader *)&heap[new_offset];
        new_block->size =
            remaining - sizeof(BlockHeader); // Update size of the new block.
        new_block->is_free = 1;              // Mark the new block as free.
        new_block->next =
            current->next; // Link the new block to the rest of the list.

        current->next = new_offset;
        current->size = size;
      }

      current->is_free = 0; // Mark the block as allocated.
      return &heap[current_offset +
                   sizeof(BlockHeader)]; // Return pointer to usable memory.
    }

    current_offset = current->next;
    if (current_offset == 0) {
      break; // Reached the end of the list.
    }
  }

  // No suitable block found.
  return NULL;
}

// free implementation with coalescing.
void my_free(void *ptr) {
  if (!ptr) {
    return;
  }

  uint8_t block_offset = (uint8_t *)ptr - heap - sizeof(BlockHeader);
  BlockHeader *block = (BlockHeader *)&heap[block_offset];
  block->is_free = 1;
}

void coalesce_memory() {
  BlockHeader *block =
      (BlockHeader *)heap; // Start from the beginning of the heap.

  while (block->next != 0) { // Traverse until the last block.
    BlockHeader *next_block = (BlockHeader *)&heap[block->next];

    if (block->is_free && next_block->is_free) {
      // Coalesce current block with the next block.
      block->size += sizeof(BlockHeader) + next_block->size;
      block->next = next_block->next; // Link to the next-next block.
    } else {
      block = next_block; // Move to the next block.
    }
  }
}

// Debug function to print the heap state.
void print_heap() {
  uint8_t current_offset = free_list;

  printf("Heap state:\n");
  while (current_offset < HEAP_SIZE) {
    BlockHeader *current = (BlockHeader *)&heap[current_offset];
    printf("Block at offset %u: size=%u, is_free=%d, next=%u\n", current_offset,
           current->size, current->is_free, current->next);

    current_offset = current->next; // Move to the next block in the list.
    if (current_offset == 0) {
      break; // End of the list.
    }
  }
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

int main() {
  init_heap();
  dump();

  void *a = my_malloc(20);
  dump();
  void *b = my_malloc(30);
  print_heap();
  dump();

  my_free(a);
  print_heap();
  dump();

  void *c = my_malloc(10);
  print_heap();
  dump();

  my_free(b);
  print_heap();
  dump();
  coalesce_memory();
  dump();

  return 0;
}
