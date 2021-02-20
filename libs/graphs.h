//
// Created by teacup123123 on 2/6/2021.
//

#ifndef STARTATC_PY_GRAPHS_H
#define STARTATC_PY_GRAPHS_H

inline void build_undirected(vpi &from, vector<vi> &into) {
    trav(p, from) {
        into[p.first].eb(p.second);
        into[p.second].eb(p.first);
    }
}

#endif //STARTATC_PY_GRAPHS_H
