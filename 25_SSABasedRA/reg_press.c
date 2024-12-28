#include <stdio.h>

double compute(int n, double x) {
    double a = 1.0, b = 2.0, c = 3.0, d = 4.0, e = 5.0;
    double f = 6.0, g = 7.0, h = 8.0, i = 9.0, j = 10.0;

    for (int k = 0; k < n; ++k) {
        // Complex formula with dependencies
        a = a + b * c;
        b = b - c / d;
        c = c + e * f - g;
        d = d * h / i;
        e = e + j - a;
        f = f - b + c * d;
        g = g * e - f / a;
        h = h + g / b;
        i = i - a * c + e;
        j = j + d - f * g;
    }

    // Return some combination to prevent dead code elimination
    return a + b + c + d + e + f + g + h + i + j;
}

int main() {
    int n = 1000000; // Large number of iterations to emphasize register usage
    double x = 3.14159;
    printf("Result: %f\n", compute(n, x));
    return 0;
}
