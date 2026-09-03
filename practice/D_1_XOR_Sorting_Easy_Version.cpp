#include <bits/stdc++.h>
#include <cassert>

using namespace std;
using ll = long long;

#define all(x) (x).begin(), (x).end()
#define sz(x) (int)(x).size()
#define pb push_back

mt19937 rnd(chrono::steady_clock::now().time_since_epoch().count());

void solve() {
    int n, q; cin >> n >> q;
    vector<int> a(n);
    for (auto &u : a) cin >> u;
    if (is_sorted(all(a))) {
        cout << "0\n";
        return;
    }
    for (int x = 0;; x++) {
        int mx = -1;
        bool good = 1;
        for (int j = 0; j * (1 << (x+1)) < n; j++) {
            int cmx = -1;
            for (int i = 0; j * (1<<(x+1)) + i < n && i < (1<<(x+1)); i++) {
                int cur = a[j *(1<<(x+1)) + i];
                good &= (mx <= cur);
                cmx = max(cmx, cur);
            }
            mx = max(mx, cmx);
        }
        if (good) {
            cout << (1<<x) << '\n';
            return;
        }
    }
}

signed main() {
    cin.tie(0)->sync_with_stdio(false);
    int tt = 1;
    cin >> tt;

    while (tt--) {
        solve();
    }

    return 0;
}