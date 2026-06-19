#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n, m;
    cin >> n >> m;

    if (m < n - 1 || m > 2 * (n + 1)) {
        cout << -1 << '\n';
        return;
    }

    string ans;

    while (n > 0 || m > 0) {

        if (m > n) {
            ans += '1';
            m--;

            if (m > n) {
                ans += '1';
                m--;
            }

            if (n > 0) {
                ans += '0';
                n--;
            }
        }
        else {
            if (n > 0) {
                ans += '0';
                n--;
            }

            if (m > 0) {
                ans += '1';
                m--;
            }
        }
    }

    cout << ans << '\n';
}

int main() {
    solve();
    return 0;
}