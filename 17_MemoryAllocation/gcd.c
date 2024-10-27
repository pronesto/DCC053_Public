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
