#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n;
        cin >> n;

        vector<long long> a(n);
        for (auto &x : a) cin >> x;

        unordered_map<long long, int> cnt1;
        unordered_map<long long, long long> cnt2;

        long long x = a[0];

        unordered_set<long long> s;
        long long c = 0;

        // insert all the possible states and keep a track of their frequencies. Whichever number's frequency is n, find its cost. Minimize this cost.
        while (!s.count(x)) {
            cnt1[x]++;
            cnt2[x] += c;

            s.insert(x);

            if (x & 1)
                x++;
            else
                x >>= 1;

            c++;
        }

        for (int i = 1; i < n; i++) {
            x = a[i];

            unordered_set<long long> s;
            c = 0;

            while (!s.count(x)) {
                if (cnt1.count(x)) {
                    cnt1[x]++;
                    cnt2[x] += c;
                }

                s.insert(x);

                if (x & 1)
                    x++;
                else
                    x >>= 1;

                c++;
            }
        }

        long long ans = 1e18;

        for (auto &[k, v] : cnt1) {
            if (v == n) {
                ans = min(ans, cnt2[k]);
            }
        }

        cout << ans << '\n';
    }

    return 0;
}