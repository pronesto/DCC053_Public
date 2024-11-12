#include <stdio.h>

int fact(int n) {
  int r = n;
  while (n > 1) {
    --n;
    r *= n;
  }
  return r;
}

int main() {
  printf("%d, %d\n", 3, fact(3));
  printf("%d, %d\n", 6, fact(6));
  printf("%d, %d\n", 10, fact(10));
}
