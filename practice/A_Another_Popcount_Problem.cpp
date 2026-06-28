#include <bits/stdc++.h>
using namespace std;

using ll = long long;

void solve() {
    ll n;
    ll k;
    cin >> n >> k;

    ll ans = 0;
    ll budget = n;

    for (int bit = 0; bit <= 60; bit++) {
        ll cost = 1LL << bit;
        if (cost > budget) break;

        ll take = min(k, budget / cost);
        ans += take;
        budget -= take * cost;
    }

    cout << ans << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) solve();
}