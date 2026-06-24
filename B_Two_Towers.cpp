#include <bits/stdc++.h>
using namespace std;

void solve() {
    long long a, b, c, d;
    cin >> a >> b >> c >> d;

    long long paired = max(0LL, min(c, d) - max(a, b));

    long long ans = (c - a) + (d - b) - paired;

    cout << ans << '\n';
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while (t--) solve();
}