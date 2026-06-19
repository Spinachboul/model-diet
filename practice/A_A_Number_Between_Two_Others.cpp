#include <bits/stdc++.h>
using namespace std;

# define lli long long int


void solve(){
    lli a, b;
    cin >> a >> b;
    if(b == 2*a){
        cout << "NO\n";
    }
    else cout << "YES\n";

}

int main(){
    int t;
    cin >> t;
    while(t--){
        solve();
    }
}