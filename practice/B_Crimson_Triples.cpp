#include <bits/stdc++.h>
using namespace std;

void solve() {
    // gcd(lcm(a,b),lcm(b,c))=gcd(a,c), 
    // we need to choose number of ways to find a,b and c
    int n;
    cin >> n;
    long long ans = 0;
    for(int i=1 ; i<=n ; i++){
        long long c = n/i;
        ans += c * c;
    }
    cout << ans << endl;

}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--)
        solve();
}