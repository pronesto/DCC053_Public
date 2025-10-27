int static_array(
    int A,
    int B,
    int C,
    int x[A],
    int y[A][B],
    int z[A][B][C],
    int a,
    int b,
    int c,
    int d,
    int e,
    int f
) {
    return x[a] + y[b][c] + z[d][e][f];
}

/*
int main() {
  int v[3];
  v[2] = 3;
  printf("%d\n", v[2]);
  *(v + 2) = 5;
  printf("%d\n", v[2]);
  *(2 + v) = 7;
  printf("%d\n", v[2]);
  2[v] = 11;
  printf("%d\n", v[2]);
}
*/
