#include <bits/stdc++.h>
using namespace std;

# define int long long
# define vi vector<int>
# define pb push_back
# define all(x) (x).begin(), (x).end()
# define sz(x) (int)(x).size()

int power(int a, int b){
    int res = 1;
    while(b){
        if(b & 1) res *= a;
        a *= a;
        b >>= 1;
    }
    return res;
}

int gcd(int a, int b){
    if(b == 0) return a;
    return gcd(b, a % b);
}
int lcm(int a, int b){
    return (a / gcd(a, b)) * b;
}
int modpow(int a, int b, int m){
    a %= m;
    int res = 1;
    while(b){
        if(b & 1) res = (res * a) % m;
        a = (a * a) % m;
        b >>= 1;
    }
    return res;
}


void solve(){
    cout << "Hello World\n";
}
int32_t main(){
    int t;
    t = 1;
    cin >> t;
    while(t--){
        solve();
    }
}