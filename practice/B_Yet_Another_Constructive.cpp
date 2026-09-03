#include <bits/stdc++.h>
using namespace std;

void solve() {
    long long n, k, m;
    cin >> n >> k >> m;

    if (k > m) {
        cout << "NO\n";
        return;
    }
    
    if (m == 1 && k > 1) {
        cout << "NO\n";
        return;
    }

    cout << "YES\n";
    if (k == 1) {
        cout << m;
        for (int i = 1; i < n; i++) {
            cout << " " << m + 1;
        }
        cout << "\n";
    } else {
        for (int i = 1; i <= n; i++) {
            if (i % k == 0) {
                cout << m - k + 1;
            } else {
                cout << 1;
            }
            cout << (i == n ? "" : " ");
        }
        cout << "\n";
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