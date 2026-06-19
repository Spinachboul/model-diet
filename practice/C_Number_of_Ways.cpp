#include<bits/stdc++.h>
using namespace std;

typedef long long ll;
typedef vector<int> vi;
typedef vector<ll> vll;
typedef pair<int,int> pii;

// macros
# define fastio() ios_base::sync_with_stdio(false);cin.tie(NULL)
# define pb push_back
# define all(x) (x).begin(),(x).end()

// constants
const ll MOD = 1e9+7;
const ll INF = 1e18;

// bit manipulation


// check if ith bit is set
bool isSet(ll n, int i){
    return (n & (1LL << i));
}




void solve(){
    ll n;
    cin >>n;

    vll cnt(n, 0);
    vll v(n);
    for(ll i=0 ; i<n ; i++){
        cin >> v[i];
    }

    ll sum = 0;
    for(ll i=0 ; i<n ; i++){
        sum = sum + v[i];
    }

    if(sum % 3 != 0){
        cout << "0" << endl;
        return;
    }

    else{
        ll s = sum/3;
        ll ss = 0;
        for(ll i=n-1 ; i>=0 ; i--){
            ss += v[i];
            if(ss == s){
                cnt[i] = 1;
            }
        }

        for(int i=n-2 ; i>=0 ; i--){
            cnt[i] += cnt[i+1];
        }

        ll ans = 0;
        ss = 0;
        for(ll i=0 ; i<n-2 ; i++){
            ss += v[i];
            if(ss == s) ans += cnt[i+2];
        }

        cout << ans << endl;
        return;


    }

}


int main(){
    int tt;
    tt = 1;
    // cin >> tt;
    while(tt--) solve();
}