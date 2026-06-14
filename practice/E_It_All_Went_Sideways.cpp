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

    lli sum = 0, maxi = -1;
    for(int i=0 ; i<n ; i++){
        cin >> v[i];
        maxi = max(maxi, v[i]);
        sum += v[i];
    }
    
    vlli suffix = v;
    for(int i=n-2; i>=0 ; i--){
        suffix[i] = min(suffix[i+1], suffix[i]);
    }

    // for(int i=0 ; i<n; i++){
    //     cout << suffix[i] << " ";
    // }

    // cout << endl;

    int longestEqual = 1;
    int len = 1;
    for(int i=0 ; i+1<n ; i++){
        if(suffix[i] == suffix[i+1]){
            ++len;
            longestEqual = max(longestEqual, len);

        }
        else{
            len = 1;
        }
    }
    lli suffixSum = 0;
    for(int i=0 ; i<n ; i++){
        suffixSum += suffix[i];
    }

    cout << (sum - suffixSum) + longestEqual - 1 << endl;



    




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

