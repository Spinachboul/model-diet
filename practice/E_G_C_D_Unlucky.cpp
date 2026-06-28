#include <bits/stdc++.h>
using namespace std;
# define lli long long int


void solve(){
    lli n;
    cin >> n;
    vector<lli> p(n), s(n);

    for(lli i=0 ; i<n ; i++){
        cin >> p[i];
    }
    for(lli i=0 ; i<n ; i++){
        cin >> s[i];
    }
    if(n==1){
        if(p[0] == s[0]){
            cout << "YES" << endl;
            return;
        }
        else{
            cout << "NO" << endl;
            return;
        }
    }

    for(lli i=0 ; i+1<n ; i++){
        if((p[i] < p[i+1]) || (s[i] > s[i+1])){
            cout << "NO" << endl;
            return;
        }
    }

    for(lli i=0 ; i+1<n ; i++){
        if(p[i] % p[i+1] != 0){
            cout << "NO" << endl;
            return;
        }
    }
    for(int i=n-1 ; i-1>=0 ; i--){
        if(s[i] % s[i-1] != 0){
            cout << "NO" << endl;
            return;
        }
    }

    if(p[n-1] != s[0]){
        cout << "NO" << endl;
        return;
    }

    for(lli i=0 ; i<n ; i++){
        lli g = gcd(p[i], s[i]);
        lli x = (p[i] / g) * s[i];

        if(i>0){
            if(gcd(x, p[i-1]) != p[i]){
                cout << "NO" << endl;
                return;
            }
        }

        if(i+1<n){
            if(gcd(x, s[i+1]) != s[i]){
                cout << "NO" << endl;
                return;
            }
        }
    }

    cout << "YES" << endl;

}

int main(){
    int t;
    cin >> t;
    while(t--) solve();
}