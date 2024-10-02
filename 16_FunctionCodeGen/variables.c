#include <stdio.h>

int global_var = 17;

int non_init_gb;

int fun(int parameter) {
  printf("%p, %lu, parameter\n", &parameter, (size_t)&parameter % 100);
  int local_fun = parameter + 1;
  printf("%p, %lu, local_fun\n", &local_fun, (size_t)&local_fun % 100);
  return 7 * local_fun;
}

int main() {
  printf("%p, %lu, global_var\n", &global_var, (size_t)&global_var % 100);
  int local_main = global_var + 13;
  printf("%p, %lu, local_main\n", &local_main, (size_t)&local_main % 100);
  non_init_gb = fun(5 * local_main);
  return 3 * non_init_gb;
}
