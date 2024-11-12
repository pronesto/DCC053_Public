#include <stdio.h>
#include <stdlib.h>

/*
 * Computes the greatest common divisor between two integer numbers.
 */
int answer = 0;

void gcd(int m, int n) {
  if (n > m) {
    gcd(n, m);
  } else if (m == n) {
    answer = m;
  } else {
    int aux = m - n;
    gcd(n, aux);
  }
}

int main(int argc, char** argv) {
  if (argc != 3) {
    fprintf(stderr, "Syntax: %s num0 num1\n", argv[0]);
    return 1;
  } else {
    int m = atoi(argv[1]);
    int n = atoi(argv[2]);
    gcd(m, n);
    printf("GCD = %d\n", answer);
    return 0;
  }
}
