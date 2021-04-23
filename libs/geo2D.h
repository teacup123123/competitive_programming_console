//
// Created by tchang on 4/23/2021.
//

#ifndef COMPETETIONS_GEO2D_H
#define COMPETETIONS_GEO2D_H

template<class T>
T &operator*(vector <vector<T>> &v, pi const &idx) {
    return v[idx.first][idx.second];
}


bool ingrid(pi xy, pi dim) {
    int x = xy.first, y = xy.second;
    int xx = dim.first, yy = dim.second;
    return x < xx and x >= 0 and y < yy and y >= 0;
}

vpi nwse(pi xy) {
    vpi ans;
    for (pi dxy:{mp(-1, 0), mp(0, -1), mp(1, 0), mp(0, 1)})ans.emplace_back(xy + dxy);
    return ans;
}

vpi box9(pi xy) {
    vpi ans;
    f0r(di, 3)
    f0r(dj, 3)
    if (di != 0 and dj != 0)
        ans.emplace_back(xy + mp(di - 1, dj - 1));
    return ans;
}

#endif //COMPETETIONS_GEO2D_H


