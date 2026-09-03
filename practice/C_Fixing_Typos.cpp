#include <bits/stdc++.h>
# define lli long long int
# define vi vector<int>
# define vlli vector<lli>
# define pb push_back
# define MOD 1000000007
# define all(v) v.begin(),v.end()

using namespace std;

void solve(){
    string s;
    cin >> s;
    string ans = "";
    for(char& c: s){
        char c1 = ans[ans.size()-1];
        char c2 = ans[ans.size()-2];
        if(c1 >='a' && c1 <='z' && c2 >= 'a' && c2<='z'){
            if(c == c1 && c1 == c2){
                continue;
            }
        }
        char c3 = ans[ans.size()-3];
        if(c3 >= 'a' && c3 <= 'z'){
            if(c==c1 && c2 == c3){
                
            }
        }


    }
    cout << ans << endl;

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

