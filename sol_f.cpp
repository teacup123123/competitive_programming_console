//sol_f.cpp abc191
//a b c d e f
#include <bits/stdc++.h>

using namespace std;

typedef long long ll;
typedef long double ld;
typedef double db;
typedef string str;

typedef pair<int, int> pi;
typedef pair<ll, ll> pl;
typedef pair<db, db> pd;

typedef vector<int> vi;
typedef vector<bool> vb;
typedef vector<ll> vl;
typedef vector<db> vd;
typedef vector<str> vs;
typedef vector<pi> vpi;
typedef vector<pl> vpl;
typedef vector<pd> vpd;

typedef set<int> si;
typedef set<ll> sl;
typedef list<int> li;
typedef map<int, int> mii;

#define mp make_pair
#define sz(x) (int)x.size()
#define len(x) (int)x.size()
#define all(x) begin(x), end(x)
#define rall(x) (x).rbegin(), (x).rend()
#define rsz resize
#define ins insert
#define ft front()
#define bk back()
#define eb emplace_back
#define ep emplace
#define lb lower_bound
#define ub upper_bound

#define vfor(i, a, b) for (int i = (a); i < (b); ++i)
#define f0r(i, a) vfor(i,0,a)
#define rof(i, a, b) for (int i = (b)-1; i >= (a); --i)
#define r0f(i, a) rof(i,0,a)
#define trav(a, x) for (auto& a: x)
#define def(fname, rtype, args, ...) function<rtype args> fname = [__VA_ARGS__] args

#define boost() cin.tie(0),cin.sync_with_stdio(0)

template<class T>
void binstf(T &found, T a, T b, function<bool(T)> test, bool TF = true) {
    T i = a, j = b;
    bool da = test(a), db = test(b);
    if ((da != TF) or (db == TF)) {
        cerr << "---[BS: TF = " << TF << "]---" << endl;
        cerr << a << "->" << da << endl;
        cerr << b << "->" << db << endl;
    }
    while (j - i > 1) {
        T m = (i + j) / 2;
        if (test(m) == TF)
            i = m;
        else
            j = m;
    }
    found = i;
    if (not TF)
        found++;
}

template<class T>
void binsft(T &a, T b, T c, function<bool(T)> d) {
    binstf(a, b, c, d, false);
}

template<class T>
T dpow(T a, T power) {
    T result = 1;
    while (power) {
        if (power % 2)result *= a;
        power /= 2, a = a * a;
    }
    return result;
}

const ld PI = acos((ld) -1);
mt19937 rng((uint32_t) chrono::steady_clock::now().time_since_epoch().count());

template<class T>
inline bool ckmin(T &a, const T &b) {
    return b < a ? a = b, 1 : 0;
}

template<class T>
inline bool ckmax(T &a, const T &b) {
    return a < b ? a = b, 1 : 0;
}

template<class T>
bool reorder(T &a, T &b) {
    return (a > b) ? swap(a, b), 1 : 0;
}

// INPUT
template<class A>
void re(complex<A> &c);

template<class A, class B>
void re(pair<A, B> &p);

template<class A>
void re(vector<A> &v);

template<class A, size_t SZ>
void re(array<A, SZ> &a);

#define ore(type, x) type x;re(x);
#define ire(x) ore(int,x);
#define vire(x) ore(vi,x);
#define lre(x) ore(ll,x);


bool online = true;

inline void re(int &x) { if (online)scanf("%d", &x); else cin >> x; }

const int MX_STR_SZ = 20'000'000;//20 MB
char char_buffer[MX_STR_SZ];

inline void re(string &s) {
    if (online) {
        int read = scanf("%s", &char_buffer);
        s.clear();
        s.assign(char_buffer);
    } else cin >> s;
}

inline void re(char &c) {
    c = '\n';
    while (c == '\n' or c == ' ')if (online)scanf("%c", &c); else cin >> c;
}

inline void re(ll &x) { if (online)scanf("%lld", &x); else cin >> x; }

inline void re(pi &e) { if (online)scanf("%d %d", &e.first, &e.second); else cin >> e.first >> e.second; }

inline void re(pl &e) { if (online)scanf("%lld %lld", &e.first, &e.second); else cin >> e.first >> e.second; }

template<class T>
inline void re(T &x) { cin >> x; }

inline void re(db &d) {
    str t;
    re(t);
    d = stod(t);
}

inline void re(ld &d) {
    str t;
    re(t);
    d = stold(t);
}

template<class H, class... T>
inline void re(H &h, T &... t) {
    re(h);
    re(t...);
}

template<class A>
void re(complex<A> &c) {
    A a, b;
    re(a, b);
    c = {a, b};
}

template<class A, class B>
inline void re(pair<A, B> &p) { re(p.first, p.second); }

template<class A>
inline void re(vector<A> &x) { trav(a, x) re(a); }

template<class A, size_t SZ>
void re(array<A, SZ> &x) { trav(a, x) re(a); }

template<class T>
T gcd(T a, T b) {
    a = a < 0 ? -a : a;
    b = b < 0 ? -b : b;
    if (a * b == 0)
        return max(a, b);
    else return gcd(min(a, b), max(a, b) % min(a, b));
}


const int MODE107 = 1000000007;

template<class T>
T modop(T a, T mode = MODE107) {
    a = a % mode;
    if (a < 0)a += mode;
    return a;
}

template<class T>
T inv(T a, T mode = MODE107) {//This is a slow operation!!!
    T coefa = 1, coefb = 0;
    T aa = a, bb = mode;
    while (aa != 1) {
        if (aa > bb)swap(coefa, coefb), swap(aa, bb);
        T cc = bb / aa;
        bb -= cc * aa, coefb -= cc * coefa;
        swap(coefa, coefb), swap(aa, bb);
    }
    return coefa;
}


const int udlrDX[] = {-1, 1, 0, 0};
const int udlrDY[] = {0, 0, -1, 1};
vpi udlrdir = {{0,  1},
               {0,  -1},
               {-1, 0},
               {1,  0}};

#define ts to_string

str ts(char c) { return str(1, c); }

str ts(bool b) { return b ? "true" : "false"; }

str ts(const char *s) { return (str) s; }

str ts(str s) { return s; }

template<class A>
str ts(complex<A> c) {
    stringstream ss;
    ss << c;
    return ss.str();
}

str ts(vector<bool> v) {
    str res = "{";
    f0r(i, sz(v)) res += char('0' + v[i]);
    res += "}";
    return res;
}

template<size_t SZ>
str ts(bitset<SZ> b) {
    str res = "";
    f0r(i, SZ) res += char('0' + b[i]);
    return res;
}

template<class A, class B>
str ts(pair<A, B> p);

template<class T>
str ts(T v) { // containers with begin(), end()
    bool fst = 1;
    str res = "{";
    for (const auto &x: v) {
        if (!fst) res += " ";
        fst = 0;
        res += ts(x);
    }
    res += "}";
    return res;
}

template<class A, class B>
str ts(pair<A, B> p) {
    return "(" + ts(p.first) + ", " + ts(p.second) + ")";
}

// OUTPUT
template<class A>
void pr(A x) { cout << ts(x); }

template<class H, class... T>
void pr(const H &h, const T &... t) {
    pr(h);
    pr(t...);
}

void ps() { pr("\n"); } // print w/ spaces
template<class H, class... T>
void ps(const H &h, const T &... t) {
    pr(h);
    if (sizeof...(t)) pr(" ");
    ps(t...);
}

template<class T>
int sgn(T a) {
    return (a > 0) - (a < 0);
}

typedef unsigned long long ull;

auto __tic__ = chrono::high_resolution_clock::now();

void tic() {
    __tic__ = chrono::high_resolution_clock::now();
}

int toc() {
    int elapsed = chrono::duration_cast<chrono::microseconds>(chrono::high_resolution_clock::now() - __tic__).count();
    return elapsed;
}

template<class T>
inline pair<T, T> operator+(const pair<T, T> a, const pair<T, T> b) {
    return mp(a.first + b.first, a.second + b.second);
}

template<class T>
inline pair<T, T> operator-(const pair<T, T> a, const pair<T, T> b) {
    return mp(a.first - b.first, a.second - b.second);
}



/* between the <manual-imports-src> tag pair, imports
//#include "libs/test_imports.h" <-- will be commented at submission
 the contents will be injected into <python-auto-import> tag pairs
 if you wish to tweak the copy, please do cp XXX to copy into the
 <python-copy-here> tag
 */

//<manual-imports-src>
//</manual-imports-src>

//<python-autoimport-src>
//</python-autoimport-src>

//<python-copy-here>

void precalc() {
}

void solve(int ti) {//note ti is 1-indexed
    //<python-autofill-src>
    //</python-autofill-src>
}

void load_cases() {
    int T = 1;
    {
//        re(T);//<test case>
    }
    vfor(i, 1, T + 1) {
//        pr("Case #",i,": ");//Google Code jam outputs
        solve(i);
    }
    bool finished;
    finished = true;
}

int main(int argc, char *argv[]) {
    if (argc > 2)
        return 0;
    if (argc == 2)
        online = false;//<codejam-interactive>
    else
        online = true;
    precalc();//

    if (online) {
        boost();
        load_cases();
    } else {//offline
        string generator_inputs[] = {//<python-generator-in>
        };//</python-generator-in>
        string testinputs[] = {//<python-autofill-in>

R"(3
6 9 12)",
R"(4
8 2 12 6)",
R"(7
30 28 33 49 27 37 48)",
        };//</python-autofill-in>
        string testoutputs[] = {//<python-autofill-out>

R"(2)",
R"(1)",
R"(7)",
        };//</python-autofill-out>

        cout << "--- generator testing ---" << endl;
        trav(testinput, generator_inputs) {
            istringstream iss(testinput);
            cin.rdbuf(iss.rdbuf());
            load_cases();
        }

        cout << "--- local testing ---" << endl;
        trav(testinput, testinputs) {
            if (testinput.back() != '\n')testinput = testinput + '\n';
            istringstream iss(testinput);
            cin.rdbuf(iss.rdbuf());
            load_cases();
        }

        cout << "--- example answers ---" << endl;
        trav(testo, testoutputs) {
            cout << testo << endl;
        }
    }
}


/* input_injection.py
import itertools as it
# re() and res() are not defined since this is non-interactive

T_defined = 0
testcases = []

with open('cf.cpp', 'r') as f:
    lines = f.readlines()
    for line in lines:
        if '//<test case>' in line:
            T_defined = not line.startswith('//')
            break


def build_testcase(params):  # TODO change the parameter here
    # TODO generate the content for the format
    testcase = []
    # ------------------------------------------------------
    n = params
    testcase.append(f'''{" ".join(f"{p}" for p in params)}''')
    # testcase.append(f'''more lines to follow''')
    # testcase.append(f'''more lines to follow''')
    # testcase.append(f'''more lines to follow''')

    # ------------------------------------------------------
    return '\n'.join(testcase)


# TODO scan the parameters
for params in it.product(*[[],]):
    testcases.append(build_testcase(params))

if T_defined:
    print(f'\t{len(testcases)}')
    for tc in testcases:
        print(tc)
else:
    for tc in testcases:
        print('\t' + tc)

input_injection.py */

void shorcuts() {
    auto x = main;//simulate online/offline mode
    load_cases();//change re(T); or add codejam print
    solve(1);//start coding
}