#include <stdio.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("Usage: %s <input_string>\n", argv[0]);
        return 1;
    }

    char *input = argv[1];
    int count = 0;

    while (input[count] != '\0') {
        count++;
    }

    printf("The input string '%s' has %d characters.\n", input, count);

    return 0;
}
