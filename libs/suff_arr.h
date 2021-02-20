//
// Created by teacup123123 on 1/15/2021.
//

#ifndef STARTCF_PY_SUFF_ARR_H
#define STARTCF_PY_SUFF_ARR_H

template<class T>
class SuffArr {
public:
    vector <vi> pow2ranks;
    int loop;
    int n;

    SuffArr() {}

    SuffArr(vector <T> &in, int loop_) {
        reset(in, loop_);
    }

    SuffArr(string &in, int loop_) {
        vector <T> cached;
        trav(c, in)
        cached.emplace_back(c);
        reset(cached, loop_);
    }

    void reset(string &in, int loop_) {
        vector <T> cached;
        trav(c, in)
        cached.emplace_back(c);
        reset(cached, loop_);
    }

    void reset(vector <T> &in, int loop_) {//N chars in charspace K
        loop = loop_, n = in.size();
        pow2ranks.clear();
        {
            vector <pair<T, int>> initial;
            map <T, queue<int>> shelf;
            f0r(i, n)
            shelf[in[i]].emplace(i);//logK per write, NlogK
            for (pair<const T, queue < int>> &kv:shelf) {
                auto &block = kv.second;
                while (not block.empty())
                    initial.emplace_back(kv.first, block.front()), block.pop();
            }
            int uid = 0, val = initial[0].first;
            pow2ranks.emplace_back(), pow2ranks.back().resize(n);
            trav(e, initial)
            {//N
                if (val < e.first)uid++;
                pow2ranks[0][e.second] = uid, val = e.first;
            }
        }
        int pow = 0, sz = 1;
        vector < queue < pair < pi, int>>> shelf(n);//(rank1,rank2),index
        while (sz < n) {//logN loops
            int newpow = pow + 1, newsz = sz * 2;
            pow2ranks.emplace_back(), pow2ranks.back().resize(n);
            auto &oldrank = pow2ranks[pow], &newrank = pow2ranks[newpow];
            vector <pair<pi, int>> tobesorted;
            f0r(i, n)
            { //N
                int j = sanitize(i + sz);
                tobesorted.emplace_back(mp(mp(oldrank[i], oldrank[j]), i));
            }
            trav(e, tobesorted)
            shelf[e.first.second].emplace(e);//N
            tobesorted.clear();
            trav(block, shelf)
            while (not block.empty()) {
                auto e = block.front();
                block.pop();
                tobesorted.emplace_back(e);
            }
            trav(e, tobesorted)
            shelf[e.first.first].emplace(e);//N
            tobesorted.clear();
            trav(block, shelf)
            while (not block.empty()) {
                auto e = block.front();
                block.pop();
                tobesorted.emplace_back(e);
            }
            int uid = 0;
            pi val = tobesorted[0].first;
            trav(e, tobesorted)
            {
                if (val < e.first)uid++;
                newrank[e.second] = uid, val = e.first;
            }
            pow = newpow, sz = newsz;
        }
    }

    inline int sanitize(int i) {
        int excess = max(i - n + 1, 0);
        i -= ((excess % loop > 0) + (excess / loop)) * loop;
        return i;
    }

    inline pair<int, int> query(int i, int len = -1) {//log len time
        i = sanitize(i);
        if (len == -1) {
            return mp(pow2ranks.back()[i], pow2ranks.back()[i]);
        }
        if (len == 0) {
            return mp(0, 0);
        } else {
            int sz = 1, pow = 0;
            while ((sz << 1) < len)sz = sz << 1, pow++;//log len time
            int j = sanitize(i + len - sz);
            return mp(pow2ranks[pow][i], pow2ranks[pow][j]);
        }
    }
};


#endif //STARTCF_PY_SUFF_ARR_H
