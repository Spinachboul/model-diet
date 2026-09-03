#include <iostream>
#include <vector>
#include <algorithm>
#include <climits>
#include <string>

using namespace std;

// Potential function: calculates the isolated game moves for a single number 'y'
unsigned long long f(unsigned long long y) {
    if (y == 0) return 0;
    unsigned long long bits = 64 - __builtin_clzll(y);
    unsigned long long ones = __builtin_popcountll(y);
    return bits + ones - 1;
}

// Finds the minimum moves (increment cost + game cost) to transition 'x' to a multiple of 2^k
unsigned long long C(unsigned long long x, int k) {
    unsigned long long power = 1ULL << k;
    unsigned long long y0;
    
    if (x == 0) {
        y0 = power;
    } else {
        y0 = ((x + power - 1) / power) * power;
    }
    if (y0 == 0) y0 = power; // Must remain strictly positive
    
    unsigned long long min_cost = ULLONG_MAX;
    
    // Check candidates. Mathematical bounds guarantee y - y0 never needs to exceed ~62.
    for (unsigned long long c = 0; ; ++c) {
        if (c > 0 && c * power > 70ULL) break;
        
        unsigned long long y = y0 + c * power;
        unsigned long long cost = (y - x) + f(y);
        
        if (cost < min_cost) {
            min_cost = cost;
        }
    }
    return min_cost;
}

void solve() {
    int n_input;
    if (!(cin >> n_input)) return;
    
    vector<unsigned long long> a;
    for (int i = 0; i < n_input; ++i) {
        unsigned long long x;
        cin >> x;
        // Ignore 0s entirely since they are erased automatically at no move penalty
        if (x > 0) {
            a.push_back(x);
        }
    }
    
    int n = a.size();
    if (n == 0) {
        cout << 0 << "\n";
        return;
    }
    
    unsigned __int128 min_total_cost = -1; // Acts as max value
    
    // Check for target collective trailing zeros up to 62
    for (int k = 0; k <= 62; ++k) {
        unsigned __int128 current_cost = 0;
        for (int i = 0; i < n; ++i) {
            current_cost += C(a[i], k);
        }
        
        // Subtract savings brought by 'k' global halves acting upon all n elements
        unsigned __int128 subtract = (unsigned __int128)1 * (n - 1) * k;
        current_cost -= subtract;
        
        if (current_cost < min_total_cost) {
            min_total_cost = current_cost;
        }
    }
    
    // Print logic formatting for massive bounds (unsigned __int128 handling string translation)
    string ans = "";
    if (min_total_cost == 0) {
        ans = "0";
    } else {
        unsigned __int128 temp = min_total_cost;
        while (temp > 0) {
            ans += (char)('0' + (temp % 10));
            temp /= 10;
        }
        reverse(ans.begin(), ans.end());
    }
    cout << ans << "\n";
}

int main() {
    // Optimizing Standard I/O Operations for speed
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    
    // Processes Inputs (Handles standalone and implicitly-grouped batch EOF structures alike)
    int t;
    if (cin >> t) {
        while (t--) {
            solve();
        }
    }
    
    return 0;
}