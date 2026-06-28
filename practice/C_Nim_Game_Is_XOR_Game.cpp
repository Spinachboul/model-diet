#include <iostream>
#include <vector>
#include <cstring>

using namespace std;

long long MOD = 998244353;
int N;
long long A[20];
long long S;
long long memo[32][1 << 15];

long long dp(int bit, int mask) {
    if (bit < 0) return 1;
    if (memo[bit][mask] != -1) return memo[bit][mask];

    long long count = 0;
    int target_xor = (S >> bit) & 1;

    // Iterate over all possible combinations of bits for b_1...b_n
    for (int i = 0; i < (1 << N); ++i) {
        int current_xor = 0;
        for (int j = 0; j < N; ++j) {
            if ((i >> j) & 1) current_xor ^= 1;
        }

        if (current_xor != target_xor) continue;

        int next_mask = 0;
        bool possible = true;
        for (int j = 0; j < N; ++j) {
            int b_bit = (i >> j) & 1;
            int a_bit = (A[j] >> bit) & 1;

            if (((mask >> j) & 1) && (b_bit > a_bit)) {
                possible = false;
                break;
            }
            if (((mask >> j) & 1) && (b_bit < a_bit)) {
                // Constraint lifted for this index
            } else {
                next_mask |= (mask & (1 << j));
            }
        }

        if (possible) {
            count = (count + dp(bit - 1, next_mask)) % MOD;
        }
    }
    return memo[bit][mask] = count;
}

void solve() {
    cin >> N;
    S = 0;
    for (int i = 0; i < N; ++i) {
        cin >> A[i];
        S ^= A[i];
    }

    if (S == 0) {
        cout << 0 << endl;
        return;
    }

    memset(memo, -1, sizeof(memo));
    // Calculate total ways to get XOR sum = S, then subtract 1 for the b=0 case
    // The b=0 case is only valid if S=0, which we already handled.
    cout << dp(30, (1 << N) - 1) << endl;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int t;
    cin >> t;
    while (t--) {
        solve();
    }
    return 0;
}