//
// Created by tchang on 2/8/2021.
//

#ifndef CODEJAM_SEGTREE_H
#define CODEJAM_SEGTREE_H

template<class T>
class segtree {
    /*
     * read-only (update O(n) impractical)
     * memory O(nlogn) built in O(nlogn)
     * segment_op O(1)!!!!
     * compatible with min,max,lcm(n=1),(gcd n=0); for + please use fenwick tree?
     */


    const T neutral;
    function<T(T, T)> fun;
    map<int, int> dlog2;
public:
    vector <vector<T>> funtable;

    segtree(function<T(T, T)> fun_, T neutral_, vector <T> src) : neutral(neutral_), fun(fun_) {
        int n = src.size();
        funtable = {src};
        int sz = 1, pow = 0;
        dlog2[sz] = pow;
        while (sz * 2 <= src.size()) {
            funtable.emplace_back();
            auto &from = funtable[sz(funtable) - 2];//size = n-sz+1
            auto &into = funtable.back();// will become n-sz*2+1
            for (int i = 0; i < n - 2 * sz + 1; i++)into.emplace_back(fun(from[i], from[i + sz]));
            sz *= 2, pow++;
            dlog2[sz] = pow;// used for lower bound, e.g. 5->8:3
        }
        dlog2[sz * 2] = pow + 1;
    }

    ll segment_op(int i, int j) {//[i,j[ convention
        int diff = j - i;
        if (diff == 0) return neutral;
        auto ptr = dlog2.lower_bound(diff);
        int pow = ptr->second - (ptr->first != diff);
        int sz = ptr->first >> (ptr->first != diff);
        return fun(funtable[pow][i], funtable[pow][j - sz]);
    }

};

#endif //CODEJAM_SEGTREE_H
