#include <stdio.h>
#include <unistd.h>
#include <sys/mman.h>

int main() {
    unsigned long kernel_start = 0xFFFFFFFF80000000; // Example address (depends on your architecture)
    printf("Kernel memory likely starts at: %lx\n", kernel_start);

    // Attempting to mmap() a kernel address will typically result in an error
    void *addr = mmap((void *)kernel_start, 4096, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    if (addr == MAP_FAILED) {
        printf("Cannot mmap kernel memory: Permission denied\n");
    } else {
        printf("Mapped kernel memory at %p (unexpected!)\n", addr);
    }

    return 0;
}

