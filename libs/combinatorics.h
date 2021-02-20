//
// Created by teacup123123 on 1/17/2021.
//

#ifndef STARTCF_PY_COMBINATORICS_H
#define STARTCF_PY_COMBINATORICS_H

//T is either int or long long usually
template<class T>
inline T lst(T t) { return t & (-t); }

template<class T>
T next_choose(T x) {
    T lstx = lst(x);
    T y = x + lstx;
    unsigned long long affected = x ^y;
    T tail = ((affected >> 2) & affected);
    T tail1 = ((affected >> 1) & affected);
    T carry = affected - tail1;
    return x + carry - tail1 + tail / lstx;
}

void demo_next_choose() {
    for (int chosen = 1; chosen < 6; chosen++) {
        ll choose = 0;
        f0r(_, chosen)
        choose <<= 1, choose++;
        for (; choose < (1LL << 14); choose = next_choose(choose)) {
            ps(std::bitset<64>(choose));
        }
    }
}

//https://www.internalpointers.com/post/writing-custom-iterators-modern-cpp

#endif //STARTCF_PY_COMBINATORICS_H
