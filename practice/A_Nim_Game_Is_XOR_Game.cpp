#include <bits/stdc++.h>
using namespace std;

const long long MOD = 998244353;

void solve(){
    int n;
    cin >> n;
    long long x= 0;
    vector<long long > v(n);
    for(int i=0 ; i<n ; i++){
        cin >> v[i];
        x ^= v[i];
    }

    if(n==1){
        cout << 0 << endl;
        return;
    }

    if(x==0){
        cout << 1 << endl;
        return;
    }

    int ans = 0;
    for(int i=0 ; i<n ; i++){
        if((v[i] ^ x) <= v[i]) ++ans;
    }

    cout << ans % MOD << endl;
    




}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;
    while(t--){
        solve();
    }
}