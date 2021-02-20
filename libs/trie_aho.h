//
// Created by teacup123123 on 1/15/2021.
//

#ifndef STARTCF_PY_AHO_H
#define STARTCF_PY_AHO_H

struct trie;

struct trie_node {
    trie *trieset;
    const int parent;
    const int link;
    const int id;

    trie_node(trie *trie_, int parent_, int link_);
};

struct trie {
    vector<trie_node> heap;//all nodes ever declared
    vector<int> links;//all nodes ever declared


    trie(char ref_ = 'a', int charset_sz_ = 26) : ref(ref_), charset_sz(charset_sz_) {//explicit?
        heap.emplace_back(this, -1, -1), links.resize(charset_sz, 0);
    }

    void add(const string &word, int from = 0, int id = 0) {
        if (from >= word.length())return;
        int link = encode(word[from]);
        if (links[id * charset_sz + link] == 0) {
            heap.emplace_back(this, id, link), links.resize(sz(heap) * charset_sz);
            links[id * charset_sz + link] = sz(heap) - 1;
        }
        add(word, from + 1, links[id * charset_sz + link]);
    }


    int find(const string &word, int from = 0, int id = 0) {
        if (from >= word.length())return id;
        else {
            int link = encode(word[from]);
            if (links[id * charset_sz + link] == 0) return -1;
            else return find(word, from + 1, links[id * charset_sz + link]);
        }
    }

    char ref;//first char of charset_sz
    int charset_sz;//beware that the memory efficiency is propto this
    int encode(const char &c) {//to be overrided if more complicated schemes involved
        return c - ref;
    }

    char decode(const int &code) {//to be overrided if more complicated schemes involved
        return ref + code;
    }


    string prefix(int id) {
        list<char> lc;
        string ans = "";
        int ptr = id;
        while (true) {
            if (heap[ptr].link != -1) {
                lc.emplace_front(decode(heap[ptr].link));
                ptr = heap[ptr].parent;
            } else
                break;
        }
        trav(c, lc)ans += c;
        return ans;
    }

    static void demonstration() {
        trie tr;
        tr.add("hello");
        tr.add("world");
        tr.add("competition");
        tr.add("atcoder");
        tr.add("helsinki");
        ps(tr.find("hell"));
        ps(tr.find("helli"));
        ps(tr.find("elli"));
        ps(tr.find("ell"));
        ps(tr.find("comp"));
        ps(tr.find("petition"));
        ps(tr.find("atc"));
    }
};

trie_node::trie_node(trie *trie_, int parent_, int link_) : trieset(trie_), parent(parent_), link(link_),
                                                            id(trie_->heap.size()) {
}

/*
 * trie_node usage:
 * trie_node t;
 * t.add("somestring");
 */

class aho {
    //automaton that points always to the longest suffix
    //failure link
private:
    vector<int> tentative_link;
public:
    vector<int> next_longest_postfix;
    trie trieset;

    aho(char ref_ = 'a', int charset_sz_ = 26) {
        trieset.ref = ref_;
        trieset.charset_sz = charset_sz_;
    }

    void add(const string &word) {
        trieset.add(word);
    }

    void corasick() {
        tentative_link.clear(), next_longest_postfix.clear();
        int &charset_sz = trieset.charset_sz;

        f0r(_, trieset.links.size()) tentative_link.emplace_back(0);
        f0r(_, trieset.heap.size()) next_longest_postfix.emplace_back(0);
        queue<int> bfs;
        //not yet in bfs    :nlp undefined,  tentative_link undefined
        //in bfs            :nlp defined,    tentative_link undefined
        //popped from bfs   :nlp defined,    tentative_link defined
        {
            int empty = 0;//0
            f0r(link, trieset.charset_sz) {
                int dstid = trieset.links[empty * charset_sz + link];
                if (dstid != 0) {
                    tentative_link[empty * charset_sz + link] = dstid;
                    next_longest_postfix[dstid] = empty, bfs.emplace(dstid);
                }
            }
        }

        while (bfs.size()) {
            int id = bfs.front();
            f0r(link, trieset.charset_sz) {
                int dstid = trieset.links[id * charset_sz + link];
                int nlp = next_longest_postfix[id];
                if (dstid == 0) {
                    tentative_link[id * charset_sz + link] = tentative_link[nlp * charset_sz + link];
                } else {
                    tentative_link[id * charset_sz + link] = dstid;
                    next_longest_postfix[dstid] = tentative_link[nlp * charset_sz + link], bfs.emplace(dstid);
                }
            }
            bfs.pop();
        }
    }

    int attempt(int id, char c) {
        return tentative_link[id * trieset.charset_sz + trieset.encode(c)];
    }

    static void demonstration();
};

void aho::demonstration() {
    aho ah;
    ah.add("cat");
    ah.add("cactus");
    ah.add("usher");
    ah.add("atom");
    ah.add("tom");
    ah.corasick();

    f0r(id, ah.trieset.heap.size()) {
        string s = ah.trieset.prefix(id);
        if (s.length() == 0)s = "[empty]";
        string t = ah.trieset.prefix(ah.next_longest_postfix[id]);
        if (t.length() == 0)t = "[empty]";

        ps(id, s, "| nlp =", t);
        vector<char> empties;
        f0r(link, ah.trieset.charset_sz) {
            char c = ah.trieset.decode(link);
            int trial = ah.attempt(id, c);
            if (trial == 0)empties.eb(c);
            else ps(s, c, ah.trieset.prefix(trial));
        }
        ps(s, empties, "-> [empty]");
    }
    ps();
}

#endif //STARTCF_PY_AHO_H
