#include <iostream>
#include <vector>

using namespace std;

const long long MOD = 1000000007;
const int MAXN = 200005;
long long p2[MAXN];

void solve() {
    int n;
    cin >> n;
    
    int c_minus = 0;
    vector<pair<int, int>> pos_counts;
    
    for (int i = 0; i < n; ++i) {
        int x;
        cin >> x;
        if (x == -1) {
            c_minus++;
        } else {
            if (pos_counts.empty() || pos_counts.back().first != x) {
                pos_counts.push_back({x, 1});
            } else {
                pos_counts.back().second++;
            }
        }
    }
    
    long long E = 1, O = 0;
    if (c_minus > 0) {
        E = p2[c_minus - 1];
        O = E;
    }
    
    long long W0 = 1;
    for (size_t i = 0; i < pos_counts.size(); ++i) {
        W0 = (W0 * p2[pos_counts[i].second - 1]) % MOD;
    }
    
    long long K = 0;
    for (size_t i = 0; i + 1 < pos_counts.size(); ++i) {
        if (pos_counts[i].first + 1 == pos_counts[i+1].first) {
            K++;
        }
    }
    
    long long ans = (W0 * (E + (O * K) % MOD)) % MOD;
    cout << ans << "\n";
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    p2[0] = 1;
    for (int i = 1; i < MAXN; ++i) {
        p2[i] = (p2[i-1] * 2) % MOD;
    }
    
    int t;
    if (cin >> t) {
        while (t--) {
            solve();
        }
    }
    return 0;
}