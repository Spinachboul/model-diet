#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n;
        cin >> n;
        vector<int> arr(n);
        if(n==1) cout << 1 << endl;
        else if(n==2) cout << -1 << endl;
        else {
            vector<int> res = {3, 6, 9};
            while(res.size() < n){
                res.push_back(res.back() * 2);
            }
            for(int i=0; i<n; i++){
                cout << res[i] << " ";
            }
            cout << endl;
        }
    }

    return 0;
}