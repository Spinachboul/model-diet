#include <bits/stdc++.h>
using namespace std;

int main() {
    long long n, k;
    cin >> n >> k;

    if(n == 1){
        if(k == 0) cout << 1 << '\n';
        else cout << -1 << '\n';
        return 0;
    }

    long long m = n / 2;

    if(k < m){
        cout << -1 << '\n';
        return 0;
    }

    long long x = k - (m - 1);

    vector<long long> ans;

    ans.push_back(x);
    ans.push_back(2 * x);

    long long cur = 2 * x + 1;

    while((int)ans.size() < n){
        ans.push_back(cur++);
    }

    for(long long v : ans)
        cout << v << ' ';
}