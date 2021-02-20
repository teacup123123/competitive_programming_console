//
// Created by tchang on 2/8/2021.
//

#ifndef CODEJAM_BINSEGTREE_H
#define CODEJAM_BINSEGTREE_H


template<class T>
class binary_segtree {
    /*
     * memory nlogn
     * update logn
     * segment_op logn
     * compatible with +,min,max,lcm(n=1),(gcd n=0)
     */
    static inline T lst(T t) { return t & (-t); }

    const T neutral;
    function<T(T, T)> fun;
    map<int, int> dlog2;
public:
    vector<vector<T>> funtable;

    binary_segtree(function<T(T, T)> fun_, T neutral_, T n) : neutral(neutral_), fun(fun_) {
        funtable = {vector<T>(n, neutral_)};
        while (sz(funtable.back()) != 1) {
            funtable.eb();
            auto &todo = funtable.back();
            auto &from = funtable[sz(funtable) - 2];
            f0r(i, sz(from) / 2 + sz(from) % 2) {
                todo.eb(fun(from[i * 2], (i * 2 + 1 < sz(from)) ? from[i * 2 + 1] : neutral_));
            }
        }
        for (int i = 0, x = 1; i < funtable.size(); i++, x = x << 1)dlog2[x] = i;
    }

    binary_segtree(function<T(T, T)> fun_, T neutral_, vector<T> src) : binary_segtree(fun_, neutral_, src.size()) {
        for (int i = 0; i < src.size(); i++) update(i, src[i]);
    }

    void update(int i, T val) {
        funtable[0][i] = val;
        for (int ptr = 1; ptr < sz(funtable); ptr++) {
            i = i / 2;
            funtable[ptr][i] = fun(funtable[ptr - 1][i * 2],
                                   (i * 2 + 1 < sz(funtable[ptr - 1])) ? funtable[ptr - 1][i * 2 + 1] : neutral);
        }
    }

    ll segment_op(int i, int j) {//[i,j[ convention
        T ans = neutral;
        while (i != j) {
            int li = lst(i), lj = lst(j);
            if (li != 0 and li < lj) {
                ans = fun(ans, funtable[dlog2[li]][i / li]), i += li;
            } else {
                ans = fun(ans, funtable[dlog2[lj]][(j - lj) / lj]), j -= lj;
            }
        }
        return ans;
    }

};


#endif //CODEJAM_BINSEGTREE_H
