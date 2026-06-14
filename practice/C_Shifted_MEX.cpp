#include <bits/stdc++.h>
# define lli long long int
# define vi vector<int>
# define vlli vector<lli>
# define pb push_back
# define MOD 1000000007
# define all(v) v.begin(),v.end()

using namespace std;

void solve(){
    int n;
    cin >> n;
    vlli v(n);
    for(int i=0 ; i<n ; i++){
        cin >> v[i];
    }

    sort(all(v));
    v.erase(unique(all(v)), v.end());
    int len = 1;
    int ans = -1;
    for(int i=0 ; i<n ; i++){
        if(i+1<n && (v[i+1] - v[i] == 1)){
            ++len;
        }
        else{
            ans = max(ans, len);
            len = 1;

        }
        
    }

    cout << ans << endl;




}

int main(){
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

    int t;
    cin >> t;
    while(t--){
        solve();
    }
	
	return 0;
}

