#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;
    vector<int> a(n), b(n);
    int ssaa = 0, ssbb = 0;
    int c1 = 0, c2 = 0;

    for (int i = 0; i < n; i++) {
        cin >> a[i];
        if (a[i] == 1) ssaa++;
    }
    for (int i = 0; i < n; i++) {
        cin >> b[i];
        if (b[i] == 1) ssbb++;
    }

    for (int i = 0; i < n; i++) {
        if (a[i] == 1 && b[i] == 0) c1++;
        if (a[i] == 0 && b[i] == 1) c2++;
    }

    if (c1 == 0 && c2 == 0) {
        cout << 0 << "\n";
        return;
    }

    if (ssaa == 0 || ssbb == n) {
        cout << -1 << "\n";
        return;
    }

    if (c1 % 2 != 0) {
        cout << 1 << "\n";
    } else {
        cout << 2 << "\n";
    }
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int t;
    if (cin >> t) {
        while (t--) {
            solve();
        }
    }
    return 0;
}