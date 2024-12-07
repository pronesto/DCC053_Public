#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main() {
  char* s0 = "DCC053 is awesome!";
  printf("Addr = %p, Contents = %s\n", s0, s0);

  const size_t SIZE = strlen(s0);

  char s1[SIZE];
  strcpy(s1, s0);
  printf("Addr = %p, Contents = %s\n", s1, s1);

  char* s2 = malloc(sizeof(SIZE));
  strcpy(s2, s0);
  printf("Addr = %p, Contents = %s\n", s2, s2);

  return 0;
}
