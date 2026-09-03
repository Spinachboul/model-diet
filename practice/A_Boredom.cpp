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
    int x;
    vector<lli> points(100001, 0);
    for(int i=0 ; i<n ; i++){
        cin >> x;
        points[x] += x;
    }

    vector<lli> dp(100001, 0);
    dp[1] = points[1];

    for(int i=2; i<100001 ; i++){
        dp[i] = max(dp[i-1] , points[i] + dp[i-2]);
    }

    cout << dp[100000] << endl; 

}

int main(){
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

    int t;
    t=1;
    // cin >> t;
    while(t--){
        solve();
    }
	
	return 0;
}

