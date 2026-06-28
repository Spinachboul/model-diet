#include <bits/stdc++.h>
using namespace std;
# define lli long long int


void solve(){
    int n, m;
    cin >> n >> m;

    vector<vector<int>> v(n, vector<int> (m));
    for(int i=0 ; i<n ; i++){
        for(int j=0 ; j<m ; j++){
            char ch;
            cin >> ch;

            v[i][j] = ch - '0';
        }
    }

    int r = 0;
    for(int i=0 ; i<n ; i++){
        int ans = 0;
        for(int j=0 ; j<m ; j++){
            int num = v[i][j];
            ans ^= num;
        }
        if(ans) ++r;
    }

    int c = 0;
    for(int j=0 ; j<m ; j++){
        int ans = 0;
        for(int i=0 ; i<n ; i++){
            int num = v[i][j];
            ans ^= num;
        }
        if(ans) ++c;
    }

    cout << max(r, c) << endl;

}

int main(){
    int t;
    cin >> t;
    while(t--) solve();
}