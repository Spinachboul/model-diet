#include <bits/stdc++.h>
using namespace std;
# define lli long long int

vector<vector<int>> adj;
set<vector<int>> guilds;
void dfs(int u, int depth, vector<vector<int>> &levels){
    if ((int)levels.size() == depth) {
        levels.push_back({});

    }
    levels[depth].push_back(u);

    for(int v: adj[u]){
        dfs(v, depth+1, levels);
    }
}
void solve() {
    int n;
    cin >> n;
    adj.assign(n+1, {});
    for(int i=2; i<=n ; i++){
        int p;
        cin >> p;
        adj[p].push_back(i);
    }

    guilds.clear();

    for(int root = 1 ; root <= n ; root++){
        vector<vector<int>> levels;
        dfs(root, 0, levels);
        for(auto& guild: levels){
            guilds.insert(guild);
        }
    }

    cout << guilds.size() << "\n";

}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--)
        solve();
}