#include "suffix_array.hpp"
#include <cassert>
#include <cstdio>
#include <random>

static void check(const string& s, mt19937& rng) {
  SuffixArray A(s);
  int n = s.size();

  vector<int> ref(n);
  for (int i = 0; i < n; i++)
    ref[i] = i;
  sort(ref.begin(), ref.end(), [&](int a, int b) { return s.substr(a) < s.substr(b); });
  assert(A.sa == ref);

  for (int i = 1; i < n; i++) {
    int h = 0;
    while (ref[i] + h < n && ref[i - 1] + h < n && s[ref[i] + h] == s[ref[i - 1] + h])
      h++;
    assert(A.lcp[i] == h);
  }

  for (int t = 0; t < 5; t++) {
    int m = 1 + rng() % 3;
    string p;
    for (int j = 0; j < m; j++)
      p += char('a' + rng() % 3);

    int cnt = 0;
    for (int i = 0; i + m <= n; i++)
      cnt += s.compare(i, m, p) == 0;

    auto [l, r] = A.search(p);
    assert(r - l == cnt);
    for (int i = l; i < r; i++)
      assert(s.compare(A.sa[i], m, p) == 0);
  }
}

int main() {
  mt19937 rng(42);

  check("", rng);
  check("a", rng);
  check("banana", rng);
  check(string(50, 'a'), rng);

  for (int it = 0; it < 3000; it++) {
    int n = rng() % 40;
    string s;
    for (int i = 0; i < n; i++)
      s += char('a' + rng() % (1 + rng() % 3));
    check(s, rng);
  }

  printf("OK: todas las pruebas pasaron\n");
}
