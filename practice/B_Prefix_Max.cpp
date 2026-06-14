#include <bits/stdc++.h>
# define lli long long int
# define vi vector<int>
# define pb push_back
# define MOD 1000000007

using namespace std;

void solve(){
    int n;
    cin >> n;
    vi v(n);
    int maxi = INT_MIN;
    for(int i=0 ; i<n ; i++){
        cin >> v[i];
        maxi = max(maxi, v[i]);
    }

    cout << maxi * n << endl;

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

