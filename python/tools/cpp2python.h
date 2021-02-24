//
// Created by teacup123123 on 2/20/2021.
//

#ifndef COMPETETIONS_CPP2PYTHON_H
#define COMPETETIONS_CPP2PYTHON_H

#define wrap(code, m) f << code << "(" << m << ")"

namespace py {
    inline void tickle(ofstream &f, int &m) { wrap('i', m); }

    inline void tickle(ofstream &f, float &m) { wrap('f', m); }

    inline void tickle(ofstream &f, string &m) { wrap('s', m); }

    inline void tickle(ofstream &f, char &m) { wrap('c', m); }

    inline void tickle(ofstream &f, const char m[]) {
        f << "s(";
        for (int i = 0; i < strlen(m); i++)f << m[i];
        f << ")";
    }

    template<class ck, class cv>
    void tickle(ofstream &f, tuple <ck, cv> &m) {
        f << "T(";
        tickle(f, get<0>(m));
        tickle(f, get<1>(m));
        f << ')';
    }

    template<class ck, class cv>
    void tickle(ofstream &f, pair <ck, cv> &m) {
        f << "T(";
        tickle(f, m.first);
        tickle(f, m.second);
        f << ')';
    }


    template<class cv>
    void tickle(ofstream &f, vector <cv> &v) {
        f << "L(";
//        tickle(f, sz(v));
        trav(x, v)
        tickle(f, x);
        f << ")";
    }

    template<class cv>
    void tickle(ofstream &f, set <cv> &s) {
        f << "S(";
//        tickle(f, sz(v));
        trav(x, s)
        tickle(f, x);
        f << ")";
    }

    template<class ck, class cv>
    void tickle(ofstream &f, map <ck, cv> &m) {
        f << "M(";
//        tickle(f, sz(v));
        trav(kv, m)
        tickle(f, kv);
        f << ")";
    }


    template<class cv>
    void save(string &&saveto, cv &&v) {
        ofstream f(R"(python\t\pickles_txt\)" + saveto + ".cpptxt");
        tickle(f, v);
        f.close();
    }

}
#endif //COMPETETIONS_CPP2PYTHON_H
