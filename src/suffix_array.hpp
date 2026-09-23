#pragma once

#include <algorithm>
#include <string>
#include <utility>
#include <vector>

using namespace std;

struct SuffixArray {
  string s;
  vector<int> sa;
  vector<int> rank;

  explicit SuffixArray(string str) : s(std::move(str)) { build(); }

  int size() const { return (int)s.size(); }

private:
  void build() {
    int n = size();
    sa.resize(n);
    rank.assign(n, 0);
    if (n == 0)
      return;
    for (int i = 0; i < n; i++)
      sa[i] = i;

    sort(sa.begin(), sa.end(), [&](int a, int b) { return s[a] < s[b]; });
    regroup([&](int i) { return make_pair((int)(unsigned char)s[i], -1); });

    for (int k = 1; rank[sa[n - 1]] < n - 1; k <<= 1) {
      vector<pair<int, int>> key(n);
      for (int i = 0; i < n; i++)
        key[i] = {rank[i], i + k < n ? rank[i + k] : -1};

      sort(sa.begin(), sa.end(), [&](int a, int b) { return key[a] < key[b]; });
      regroup([&](int i) { return key[i]; });
    }
  }

  template <class KeyFn> void regroup(KeyFn key) {
    int n = size();
    vector<int> nr(n);
    nr[sa[0]] = 0;
    for (int i = 1; i < n; i++)
      nr[sa[i]] = nr[sa[i - 1]] + (key(sa[i - 1]) != key(sa[i]));
    rank = nr;
  }
};
