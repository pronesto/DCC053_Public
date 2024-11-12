// example.c
#include <stdio.h>

int main() {
    int a = 5;
    int b = 10;
    int sum;

    if (a < b) {
        sum = a + b;
    } else {
        sum = a - b;
    }

    printf("Result: %d\n", sum);
    return 0;
}
