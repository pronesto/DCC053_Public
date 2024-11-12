#include <stdio.h>

int st_fact(int n) {
  static int result = 1;
  result = n;
  result *= (result <= 1) ? 1 : st_fact(result - 1);
  return result;
}

int dy_fact(int n) {
  int result = 1;
  result = n;
  result *= (result <= 1) ? 1 : dy_fact(result - 1);
  return result;
}

int main(int argc, char** argv) {
  for (int i = 2; i < 2 * argc; ++i) {
    printf("%d: st_fact = %d, dy_fact = %d\n", i, st_fact(i), dy_fact(i));
  }
  return 0;
}
