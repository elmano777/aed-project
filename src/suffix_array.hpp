#pragma once

#include <algorithm>
#include <string>
#include <utility>
#include <vector>

using namespace std;

struct SuffixArray {
  struct Round {
    int k;
    vector<int> sa;
    vector<int> rank;
  };

  struct Step {
    bool upper;
    int lo, hi, mid;
    bool go_right;
  };

  string s;
  vector<int> sa;
  vector<int> rank;
  vector<int> lcp;
  vector<Round> rounds;

  explicit SuffixArray(string str) : s(std::move(str)) { build(); }

  int size() const { return (int)s.size(); }

  int cmp_prefix(int i, const string &p) const {
    return s.compare(i, p.size(), p);
  }

  pair<int, int> search(const string &p, vector<Step> *trace = nullptr) const {
    int n = size();

    int lo = 0, hi = n;
    while (lo < hi) {
      int mid = (lo + hi) / 2;
      bool right = cmp_prefix(sa[mid], p) < 0;
      if (trace)
        trace->push_back({false, lo, hi, mid, right});
      if (right)
        lo = mid + 1;
      else
        hi = mid;
    }
    int l = lo;

    hi = n;
    while (lo < hi) {
      int mid = (lo + hi) / 2;
      bool right = cmp_prefix(sa[mid], p) <= 0;
      if (trace)
        trace->push_back({true, lo, hi, mid, right});
      if (right)
        lo = mid + 1;
      else
        hi = mid;
    }
    return {l, lo};
  }

private:
  void build() {
    int n = size();
    sa.resize(n);
    rank.assign(n, 0);
    lcp.assign(n, 0);
    if (n == 0)
      return;
    for (int i = 0; i < n; i++)
      sa[i] = i;

    sort(sa.begin(), sa.end(), [&](int a, int b) { return s[a] < s[b]; });
    regroup([&](int i) { return make_pair((int)(unsigned char)s[i], -1); });
    rounds.push_back({0, sa, rank});

    for (int k = 1; rank[sa[n - 1]] < n - 1; k <<= 1) {
      vector<pair<int, int>> key(n);
      for (int i = 0; i < n; i++)
        key[i] = {rank[i], i + k < n ? rank[i + k] : -1};

      sort(sa.begin(), sa.end(), [&](int a, int b) { return key[a] < key[b]; });
      regroup([&](int i) { return key[i]; });
      rounds.push_back({k, sa, rank});
    }

    kasai();
  }

  void kasai() {
    int n = size();
    int h = 0;
    for (int i = 0; i < n; i++) {
      if (rank[i] > 0) {
        int j = sa[rank[i] - 1];
        while (i + h < n && j + h < n && s[i + h] == s[j + h])
          h++;
        lcp[rank[i]] = h;
        if (h > 0)
          h--;
      } else {
        h = 0;
      }
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
