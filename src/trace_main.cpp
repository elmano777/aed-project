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

  printf(",\"rounds\":[");
  for (size_t r = 0; r < A.rounds.size(); r++) {
    auto& R = A.rounds[r];
    printf("%s{\"k\":%d,\"sa\":", r ? "," : "", R.k);
    print_arr(R.sa);
    printf(",\"rank\":");
    print_arr(R.rank);
    printf("}");
  }
  printf("]");

  if (!p.empty()) {
    vector<SuffixArray::Step> steps;
    auto [l, r] = A.search(p, &steps);
    printf(",\"pattern\":\"%s\",\"range\":[%d,%d],\"steps\":[", p.c_str(), l, r);
    for (size_t i = 0; i < steps.size(); i++) {
      auto& st = steps[i];
      printf("%s{\"upper\":%s,\"lo\":%d,\"hi\":%d,\"mid\":%d,\"go_right\":%s}", i ? "," : "",
             st.upper ? "true" : "false", st.lo, st.hi, st.mid, st.go_right ? "true" : "false");
    }
    printf("]");
  }

  printf("}\n");
}
