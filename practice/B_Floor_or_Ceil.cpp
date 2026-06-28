#include <bits/stdc++.h>
using namespace std;

#define lli long long int

// Helper to find the minimum possible value
lli F(lli x, lli n){
    while(n--){
        if(!x) return x;
        x = (x >> 1);
    }
    return x;
}

lli C(lli x, lli n){
    while(n--){
        if(x <=1 ) return x;
        x = (x+1) >> 1;

    }
    return x;
}

void solve() {
    lli x, n, m;
    cin >> x >> n >> m;
    
    // We pass copies of x, n, m so the calculations don't interfere with each other
    cout << F(C(x, m), n) << " " << C(F(x, n), m) << "\n";
}

int main() {
    // Fast I/O
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    int t;
    cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}