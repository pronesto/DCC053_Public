#include <time.h>
#include <stdio.h>

int main(int argc, char** argv) {
  const int M = 4000;
  const int N = 2000;
  char m[M][N];
  int i, j, k;
  int sum = 0;
  clock_t start, end;
  double time;

  // Initializes the array:
  for (i = 0; i < M; i++) {
    for (j = 0; j < N; j++) {
      m[i][j] = (i + j) & 7;
    }
  }

  start = clock();
  printf("argc = %d\n", argc);
  if (argc % 2) {
    printf("argc is even: summing row major:");
    // Sums up the matrix elements, row major:
    for (i = 0; i < M; i++) {
      for (j = 0; j < N; j++) {
        sum += m[i][j];
      }
    }
  } else {
    printf("argc is odd: summing column major:");
    // Sums up the matrix of elements, column major:
    for (j = 0; j < N; j++) {
      for (i = 0; i < M; i++) {
        sum += m[i][j];
      }
    }
  }
  end = clock();

  time = ((double) (end - start)) / CLOCKS_PER_SEC;
  printf("sum: %d, Time: %lf\n", sum, time);
}

