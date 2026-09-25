#include "suffix_array.hpp"
#include <cstdio>

static void print_arr(const vector<int>& v) {
  printf("[");
  for (size_t i = 0; i < v.size(); i++)
    printf("%s%d", i ? "," : "", v[i]);
  printf("]");
}

int main(int argc, char** argv) {
  string s = argc > 1 ? argv[1] : "";
  string p = argc > 2 ? argv[2] : "";

  SuffixArray A(s);

  printf("{\"s\":\"%s\",\"n\":%d,\"sa\":", s.c_str(), A.size());
  print_arr(A.sa);
  printf(",\"lcp\":");
  print_arr(A.lcp);

  if (!p.empty()) {
    auto [l, r] = A.search(p);
    printf(",\"pattern\":\"%s\",\"range\":[%d,%d]", p.c_str(), l, r);
  }

  printf("}\n");
}
