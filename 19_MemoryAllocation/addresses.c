#include <stdio.h>
#include <stdlib.h>

int global_var;
int initialized_var = 42;

int main() {
    char *str = "Hello, world!";
    int local_var = 5;
    int *dynamic_var = malloc(sizeof(int));

    *dynamic_var = 10;
    printf("Address of global_var: %p\n", &global_var);
    printf("Address of initialized_var: %p\n", &initialized_var);
    printf("Address of str: %p\n", str);
    printf("Address of local_var: %p\n", &local_var);
    printf("Address of dynamic_var: %p\n", dynamic_var);

    // Print addresses of main and printf
    printf("Address of main: %p\n", (void *)main);
    printf("Address of printf: %p\n", (void *)printf);

    free(dynamic_var);
    return 0;
}
