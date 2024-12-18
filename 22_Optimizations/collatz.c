/*
 * Example taken from: https://sbaziotis.com/compilers/compiler-opt.html
 */
static int collatz(int n) {
  int its = 0;
  while (n != 1) {
    its++;
    if (n % 2 == 0) {
      n /= 2;
    } else {
      n = 3 * n + 1;
    }
  }
  return its;
}

int main(void) {
  return collatz(6);
}
