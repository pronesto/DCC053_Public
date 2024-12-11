#include <stdio.h>

typedef struct {
    int elements[100];
    int size;
} List;

// External function to get the size
int size(List* list) {
    return list->size;
}

// Main function
int main() {
    List myList = {{1, 2, 3}, 3};
    printf("Size: %d\n", size(&myList));
    return 0;
}

