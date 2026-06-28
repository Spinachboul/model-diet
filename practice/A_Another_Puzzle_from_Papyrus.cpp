#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n, c;
    cin >> n >> c;

    vector<int> a(n), b(n);
    for (int &x : a) cin >> x;
    for (int &x : b) cin >> x;

    const int INF = 1e9;

    // Case 1: Don't reorder
    int cost1 = 0;
    bool ok1 = true;
    for (int i = 0; i < n; i++) {
        if (a[i] < b[i]) {
            ok1 = false;
            break;
        }
        cost1 += a[i] - b[i];
    }

    // Case 2: Reorder once
    vector<int> sa = a, sb = b;
    sort(sa.begin(), sa.end());
    sort(sb.begin(), sb.end());

    int cost2 = c;
    bool ok2 = true;
    for (int i = 0; i < n; i++) {
        if (sa[i] < sb[i]) {
            ok2 = false;
            break;
        }
        cost2 += sa[i] - sb[i];
    }

    int ans = INF;
    if (ok1) ans = min(ans, cost1);
    if (ok2) ans = min(ans, cost2);

    if (ans == INF)
        cout << -1 << '\n';
    else
        cout << ans << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--)
        solve();
}