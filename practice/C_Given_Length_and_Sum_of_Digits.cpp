#include <bits/stdc++.h>
using namespace std;

void solve(){
        int m,s;
        cin >> m >> s;
        if(m ==1 && s == 0){
            cout << "0 0" << endl;
            return;
        }

        if(s > 9 * m || (s == 0 && m > 1)){
            cout << "-1 -1\n";
            return;
        }

        // forming the largest number
        string largest = "";
        int sum = s;

        for(int i=0; i <m ; i++){
            int digit = min(sum, 9);
            largest += char(digit + '0');
            sum -= digit;
        }

        string smallest(m, '0');
        sum = s;

        sum--;

        for(int i=m-1 ; i>=1 ; i--){
            int digit = min(sum, 9);
            smallest[i] = char(digit + '0');
            sum -= digit;
        }

        smallest[0] = char('0' + (sum+1));
        cout << smallest << " " << largest << endl;


}
int main(){
    int tt;
    tt = 1;
    // cin >> tt;
    while(tt--) solve();
}