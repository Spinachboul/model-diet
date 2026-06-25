#include<bits/stdc++.h>
#ifdef DEBUG_LOCAL
#include <mydebug/debug.h>
#endif
using ll = long long;
const int N = 5e5+5;
using namespace std;
int T,n; string s; ll a[N],c[N],b[N],d[N];
void los(){
    cin >> n >> s,s = " " + s; d[0] = 1;
    for(int i = 1;i <= n;i ++) cin >> a[i],d[i] = 0;
    for(int i = 1;i <= n;i ++) cin >> c[i];
    c[0] = -1e18,b[0] = 0;
    for(int i = 1;i <= n;i ++){
        if(c[i] != c[i - 1]){
            if(c[i] < c[i-1]) return cout << "No\n",void();
            b[i] = c[i],d[i] = 1;
            for(int j = i;j >= 0;j --){
                if(s[j] == '1'){
                    if(d[j - 1] && b[j - 1] + a[j] != b[j]) return cout << "No\n",void();
                    d[j - 1] = 1,b[j - 1] = b[j] - a[j];
                }else break;
            }
        }
    }for(int i = 1;i <= n;i ++){
        if(s[i] == '1') b[i] = b[i-1] + a[i],d[i] = 1;
        if(!d[i]) b[i] = -1e16;
        a[i] = b[i] - b[i-1];
        if(max(c[i-1],b[i]) != c[i]) return cout << "No\n",void();
    }
    cout << "Yes\n";
    for(int i = 1;i <= n;i ++){
        cout << a[i] << " \n"[i == n];
    }
}int main(){
    ios::sync_with_stdio(0),cin.tie(0);
    for(cin >> T;T --;) los();
}
