#include <stdio.h>

struct __attribute__((packed))
MyStruct {
    char c;
    long l;
    int i;
};

int main() {
    struct MyStruct s;
    char *base = (char *)&s;

    // s.c = 'A'
    *base = 'A';

    // s.l = 2 (offset 1)
    *(long *)(base + 1) = 2;

    // s.i = 3 (offset 9)
    *(int *)(base + 9) = 3;

    printf("s.c = %c\n", s.c);
    printf("s.l = %ld\n", s.l);
    printf("s.i = %d\n", s.i);

    return 0;
}

