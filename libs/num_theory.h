//
// Created by tchang on 2/5/2021.
//

#ifndef CODEJAM_PRIME_LADDER_H
#define CODEJAM_PRIME_LADDER_H

void smallest_prime_factor_ladder(vi &into) {
    trav(e, into)e = INT_MAX;
    into[0] = 1;
    into[1] = 1;
    for (int p = 2; p < sz(into); p++) {
        if (into[p] == INT_MAX) {
            into[p] = p;
            for (int x = 2 * p; x < sz(into); x += p) {
                ckmin(into[x], p);
            }
        }
    }
}

int number_of_factors(ll N, vi *smallest_prime_factor = nullptr, vi *ordered_prime_numbers = nullptr) {
    /**
     *  @brief  Copies fields of __rhs into this.
     *  @param  N  O(sqrt(N))
     *  @return  O(sqrt(N))
     *
     *  O(sqrt(N))
    */
    prime_fac_num_complexity:
    if (smallest_prime_factor != nullptr and N < smallest_prime_factor->size()) {
        map<int, int> decompo;
        while (N != 1) {
            decompo[(*smallest_prime_factor)[N]]++;
            N /= (*smallest_prime_factor)[N];
        }
        int ans = 1;
        trav(kv, decompo)ans *= kv.second + 1;
        return ans;
    }
    log_sz_primes_complexity:
    if (ordered_prime_numbers != nullptr) {
        map<int, int> decompo;
        //divide in reverse order big primes first, until acceleratable if acceleratable
        vi &primes = *ordered_prime_numbers;

        ll last = primes.back();
        if (last * last < N)goto bruteforce_sqrtN_complexity;

        while (N != 1) {
            //last*last>=N
            int a, b;
            f0r(_, 2) {
                a = -1, b = primes.size() - 1;//bad, good
                while (b != a + 1) {
                    int m = (a + b) / 2;
                    ll p = primes[m];
                    if (p * p < (_ ? N : N * N))
                        a = m;//m bad
                    else
                        b = m;//m good
                }
                if (primes[b] == N)
                    break;
            }
            b = b;
            for (; b >= 0; b--) {
                if (N % primes[b] == 0) {
                    decompo[primes[b]]++;
                    N /= primes[b];
                    break;
                }
            }
        }
        int ans = 1;
        trav(kv, decompo)ans *= kv.second + 1;
        return ans;
    }
    bruteforce_sqrtN_complexity:
    {
        ll sq = sqrt(N), ans = 0;
        while (sq * sq < N)sq++;
        while (sq * sq > N)sq--;
        for (ll i = 1; i <= sq; i++) if (N % i == 0) ans += 2;
        if (sq * sq == N) ans--;
        return ans;
    }
}

void demonstration_numfac() {
    int until = 2000000;
    vi smallest_pf(until + 2);
    vi primes;

    //start here
    smallest_prime_factor_ladder(smallest_pf);
    for (int p = 2; p < sz(smallest_pf); p++)if (smallest_pf[p] == p)primes.eb(p);
    vi sol, sol2;
    tic();
    for (int i = 1; i <= until; i++) {
        sol2.eb(number_of_factors(i, &smallest_pf));
    }
    ps(toc());
    tic();
    for (int i = 1; i <= until; i++) {
        sol2[i - 1] = number_of_factors(i, nullptr, &primes);
    }
    ps(toc());
    tic();
    for (int i = 1; i <= until; i++) {
        sol.eb(number_of_factors(i));
    }
    ps(toc());
    f0r(i, sz(sol))assert(sol[i] == sol2[i]);
}

#endif //CODEJAM_PRIME_LADDER_H
