#include <stdio.h>

int compute(int n) {
    int a = 1, b = 1, c = 2, d = 3, e = 5;
    int f = 8, g = 13, h = 21, i = 34, j = 55;

    for (int k = 0; k < n; ++k) {
        // Fibonacci-like series update
        int next = a + b + c + d + e + f + g + h + i + j;
        a = b + c;
        b = c + d;
        c = d + e;
        d = e + f;
        e = f + g;
        f = g + h;
        g = h + i;
        h = i + j;
        i = j + next;
        j = next; // Keep all variables live
    }

    // Combine results to avoid dead code elimination
    return a + b + c + d + e + f + g + h + i + j;
}

int main() {
    int n = 1000000; // Large number of iterations
    int result = compute(n);
    printf("Result: %d\n", result);
    return 0;
}
