//
// Created by teacup123123 on 1/15/2021.
//

#ifndef STARTCF_PY_FENWICK_H
#define STARTCF_PY_FENWICK_H

class fenwick {
private:
    vl data;
    vl single;
public:
    fenwick(int sz) {
        //x & -x is the LST
        // data[5<1>] = ]5-1, 5]
        data.resize(1), single.resize(1);
        while (sz(data) < sz + 1)data.resize(sz(data) * 2), single.resize(sz(data));
    }

    template<class T>
    fenwick(vector<T> &src):fenwick(src.size()) {
        f0r(i, src.size())update(i, src[i]);
    }

    ll sum(int index) {
        ll sum = 0; // Iniialize result
        // index in BITree[] is 1 more than the index in arr[]
//        index = index + 1; non-inclusive
        while (index > 0) {
            sum += data[index];
            // Move index to parent node in getSum View
            index -= index & (-index);
        }
        return sum;
    }

    void update(int index, ll val) {
        // index in BITree[] is 1 more than the index in arr[]
        index = index + 1;
        ll dval = val - single[index];
        single[index] = val;
        while (index < sz(data)) {
            // Add 'val' to current node of BI Tree
            data[index] += dval;
            // Update index to that of parent in update View
            index += index & (-index);
        }
    }

    ll sum(int i, int j) {
        return sum(j) - sum(i);
    }
};

#endif //STARTCF_PY_FENWICK_H
