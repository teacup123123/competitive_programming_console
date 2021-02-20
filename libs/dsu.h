//
// Created by teacup123123 on 2/13/2021.
//

#ifndef STARTATC_PY_DSU_H
#define STARTATC_PY_DSU_H

struct ddsu {
    vi delegate;
    vi weight;

    ddsu(int n) {
        delegate = vi(n);
        f0r(i, n)delegate[i] = i;
        weight = vi(n, 1);
    }

    void merge(int i, int j) {
        if (identity(i) != identity(j)) {
            i = identity(i), j = identity(j);
            if (weight[i] >= weight[j])swap(i, j);
            delegate[i] = delegate[j];
            weight[j] += weight[i];
        }
    }

    int identity(int i) {
        if (delegate[i] != i) {
            return delegate[i] = identity(delegate[i]);
        } else return i;
    }
};

#endif //STARTATC_PY_DSU_H
