//
// Created by teacup123123 on 2/20/2021.
//

#ifndef COMPETETIONS_PARSETXT_H
#define COMPETETIONS_PARSETXT_H


inline void parsetxt(ifstream &from, int &res) { from >> res; }

inline void parsetxt(ifstream &from, char &res) { from >> res; }

inline void parsetxt(ifstream &from, string &res) { from >> res; }

inline void parsetxt(ifstream &from, float &res) { from >> res; }

template<class a, class b>
inline void parsetxt(ifstream &from, tuple<a, b> &res) { from >> get<0>(res) >> get<1>(res); }

template<class a, class b, class c>
inline void parsetxt(ifstream &from, tuple<a, b> &res) { from >> get<0>(res) >> get<1>(res) >> get<2>(res); }

template<class ck, class cv>
void parsetxt(ifstream &from, map<ck, cv> &res);

template<class cv>
void parsetxt(ifstream &from, vector<cv> &res);


template<class ck, class cv>
void parsetxt(ifstream &from, map<ck, cv> &res) {
    res.clear();
    int len;
    from >> len;
    f0r(i, len) {
        ck k;
        parsetxt(from, k);
        cv v;
        parsetxt(from, v);
        res.emplace(k, v);
    }
}


template<class cv>
void parsetxt(ifstream &from, set<cv> &res) {
    res.clear();
    int len;
    from >> len;
    f0r(i, len) {
        cv v;
        parsetxt(from, v);
        res.emplace(v);
    }
}

template<class cv>
void parsetxt(ifstream &from, vector<cv> &res) {
    res.clear();
    int len;
    from >> len;
    res.resize(len);
    f0r(i, len) {
        parsetxt(from, res[i]);
    }
}


#endif //COMPETETIONS_PARSETXT_H
