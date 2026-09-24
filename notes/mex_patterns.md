# MEX : Maximun Excluded Element

## Summary Sheet
1. MEX ∈ [0, n]

2. MEX = k
   ↔ 0,1,...,k-1 present
   AND k absent

3. MEX ≥ k
   ↔ 0,1,...,k-1 all present

4. One-time MEX
   → frequency / boolean array

5. Dynamic MEX
   → frequency + mex
   → or set of missing values

6. Sliding window
   → add/remove frequencies + maintain mex

7. Subarray/permutation
   → think positions of 0,1,...,k-1

8. Construction
   → explicitly include 0...k-1
   → exclude k

9. XOR + MEX
   → transform "all values 0...k-1 exist"
   → investigate trie/bitwise structure

10. Split array
    → prefix_mex / suffix_mex


Absolutely. Here’s a **competitive-programming MEX template sheet in C++**, covering the variations you’re most likely to encounter.

 ## 1\. Basic MEX — O(n)

 Use when you need the MEX of an array once.

```
int mex(vector<int>& a) {
    int n = a.size();

    vector<bool> present(n + 1, false);

    for (int x : a) {
        if (0 <= x && x <= n)
            present[x] = true;
    }

    for (int i = 0; i <= n; i++) {
        if (!present[i])
            return i;
    }

    return n;
}
```

 ### Example

```
vector<int> a = {0, 1, 2, 4};

cout << mex(a); // 3
```

---

 # 2\. MEX using a frequency array

 Often preferable when you'll modify the array.

```
int n = a.size();

vector<int> freq(n + 1);

for (int x : a) {
    if (0 <= x && x <= n)
        freq[x]++;
}

int mex = 0;

while (mex <= n && freq[mex] > 0)
    mex++;

cout << mex;
```

 The important idea:

```
while (freq[mex] > 0)
    mex++;
```

---

 # 3\. MEX using a `set`

 Useful when values are dynamically inserted/deleted.

```
set<int> missing;

for (int i = 0; i <= n; i++)
    missing.insert(i);

for (int x : a) {
    if (0 <= x && x <= n)
        missing.erase(x);
}

int mex = *missing.begin();
```

 Complexity:

```
O(n log n)
```

---

 # 4\. Dynamic MEX — insert elements

 This is an important pattern.

```
vector<int> freq(n + 1);
int mex = 0;

auto add = [&](int x) {
    if (x < 0 || x > n)
        return;

    freq[x]++;

    if (x == mex) {
        while (mex <= n && freq[mex] > 0)
            mex++;
    }
};
```

 Example:

```
add(0); // mex becomes 1
add(1); // mex becomes 2
add(5); // mex remains 2
add(2); // mex becomes 3
```

---

 # 5\. Dynamic MEX — insert + erase

 This is the more complete template.

```
vector<int> freq(n + 1);
int mex = 0;

auto add = [&](int x) {
    if (x < 0 || x > n)
        return;

    freq[x]++;

    if (x == mex) {
        while (mex <= n && freq[mex] > 0)
            mex++;
    }
};

auto remove = [&](int x) {
    if (x < 0 || x > n)
        return;

    freq[x]--;

    if (freq[x] == 0 && x < mex)
        mex = x;
};
```

 This is one of the **most useful MEX templates to memorize**.

---

 # 6\. Dynamic MEX using `set` of missing values

 Sometimes this is cleaner.

```
vector<int> freq(n + 1);
set<int> missing;

for (int i = 0; i <= n; i++)
    missing.insert(i);

auto add = [&](int x) {
    if (x < 0 || x > n)
        return;

    freq[x]++;

    if (freq[x] == 1)
        missing.erase(x);
};

auto remove = [&](int x) {
    if (x < 0 || x > n)
        return;

    freq[x]--;

    if (freq[x] == 0)
        missing.insert(x);
};

auto getMex = [&]() {
    return *missing.begin();
};
```

 This gives:

```
add    O(log n)
remove O(log n)
mex    O(1)
```

---

 # 7\. MEX of every prefix

 Suppose:

```
a = [0, 2, 1, 5, 3]
```

 Find MEX after every prefix.

```
vector<int> freq(n + 1);
vector<int> prefixMex(n);

int mex = 0;

for (int i = 0; i < n; i++) {
    int x = a[i];

    if (0 <= x && x <= n)
        freq[x]++;

    while (mex <= n && freq[mex] > 0)
        mex++;

    prefixMex[i] = mex;
}
```

 Result:

```
prefix:     [0] [0,2] [0,2,1] ...
mex:         1    1      3
```

---

 # 8\. MEX of every suffix

 Calculate from right to left.

```
vector<int> freq(n + 1);
vector<int> suffixMex(n);

int mex = 0;

for (int i = n - 1; i >= 0; i--) {
    int x = a[i];

    if (0 <= x && x <= n)
        freq[x]++;

    while (mex <= n && freq[mex] > 0)
        mex++;

    suffixMex[i] = mex;
}
```

 Then:

```
suffixMex[i]
```

 = MEX of:

```
a[i ... n-1]
```

---

 # 9\. MEX of every split

 Suppose you want:

```
[0 ... i] | [i+1 ... n-1]
```

 and need both MEX values.

```
vector<int> prefMex(n);
vector<int> suffMex(n);

// Prefix MEX
{
    vector<int> freq(n + 1);
    int mex = 0;

    for (int i = 0; i < n; i++) {
        if (0 <= a[i] && a[i] <= n)
            freq[a[i]]++;

        while (mex <= n && freq[mex] > 0)
            mex++;

        prefMex[i] = mex;
    }
}

// Suffix MEX
{
    vector<int> freq(n + 1);
    int mex = 0;

    for (int i = n - 1; i >= 0; i--) {
        if (0 <= a[i] && a[i] <= n)
            freq[a[i]]++;

        while (mex <= n && freq[mex] > 0)
            mex++;

        suffMex[i] = mex;
    }
}

// Split after i
for (int i = 0; i + 1 < n; i++) {
    int leftMex = prefMex[i];
    int rightMex = suffMex[i + 1];

    // use leftMex and rightMex
}
```

 This pattern is extremely common.

---

 # 10\. MEX of every sliding window

 Suppose window size is `k`.

```
vector<int> freq(n + 1);
int mex = 0;

for (int i = 0; i < n; i++) {

    // Add a[i]
    if (0 <= a[i] && a[i] <= n) {
        freq[a[i]]++;

        if (a[i] == mex) {
            while (mex <= n && freq[mex] > 0)
                mex++;
        }
    }

    // Remove a[i-k]
    if (i >= k) {
        int x = a[i - k];

        if (0 <= x && x <= n) {
            freq[x]--;

            if (freq[x] == 0 && x < mex)
                mex = x;
        }
    }

    // Window is ready
    if (i >= k - 1) {
        cout << mex << ' ';
    }
}
```

 Complexity:

```
O(n)
```

 amortized.

---

 # 11\. MEX of every subarray — brute force

 For small constraints, the simplest solution is sometimes enough.

```
for (int l = 0; l < n; l++) {

    vector<bool> present(n + 1);

    for (int r = l; r < n; r++) {

        if (0 <= a[r] && a[r] <= n)
            present[a[r]] = true;

        int mex = 0;

        while (mex <= n && present[mex])
            mex++;

        cout << "MEX(" << l << "," << r << ") = "
             << mex << '\n';
    }
}
```

 Complexity:

```
O(n^2)
```

 plus the MEX scan.

 For small `n`, this is often perfectly fine.

---

 # 12\. MEX of a subarray using timestamp technique

 Useful when repeatedly creating `present[]`.

 Instead of clearing an array every time:

```
vector<int> seen(n + 1, 0);
int timer = 0;

for (int l = 0; l < n; l++) {

    timer++;

    for (int r = l; r < n; r++) {

        if (0 <= a[r] && a[r] <= n)
            seen[a[r]] = timer;

        int mex = 0;

        while (mex <= n && seen[mex] == timer)
            mex++;

        cout << mex << '\n';
    }
}
```

 This is a useful **implementation trick**.

---

 # 13\. Check `MEX >= k`

 This is much simpler than calculating the MEX.

```
bool mexAtLeastK(vector<int>& a, int k) {
    vector<bool> present(k);

    for (int x : a) {
        if (0 <= x && x < k)
            present[x] = true;
    }

    for (int i = 0; i < k; i++) {
        if (!present[i])
            return false;
    }

    return true;
}
```

 Because:

```
MEX >= k
⇔
0,1,2,...,k-1 are all present
```

---

 # 14\. Check `MEX == k`

```
bool mexEqualsK(vector<int>& a, int k) {

    vector<bool> present(k + 1);

    for (int x : a) {
        if (0 <= x && x <= k)
            present[x] = true;
    }

    // 0 ... k-1 must exist
    for (int i = 0; i < k; i++) {
        if (!present[i])
            return false;
    }

    // k must NOT exist
    if (present[k])
        return false;

    return true;
}
```

 Remember this equivalence:

```
MEX = k
⇔
all [0, k-1] exist
AND
k doesn't exist
```

---

 # 15\. Minimum operations to make MEX = k

 A very common type of problem.

 First count:

 - how many values from `0...k-1` are missing
- whether `k` exists

```
int operationsToMakeMexK(vector<int>& a, int k) {

    vector<int> freq(k + 1);

    for (int x : a) {
        if (0 <= x && x <= k)
            freq[x]++;
    }

    int missing = 0;

    for (int i = 0; i < k; i++) {
        if (freq[i] == 0)
            missing++;
    }

    // We need k to disappear as well.
    // Missing values can replace occurrences of k.
    return max(missing, freq[k]);
}
```

 For example:

```
a = [0, 1, 1, 4]
k = 3
```

 `2` is missing and `3` is already absent.

 Answer = `1`.

---

 # 16\. Construct an array with MEX = k

 Simplest construction:

```
vector<int> constructMexK(int n, int k) {

    vector<int> ans;

    // Put 0 ... k-1
    for (int i = 0; i < k; i++)
        ans.push_back(i);

    // Fill remaining positions with something != k
    while ((int)ans.size() < n)
        ans.push_back(k + 1);

    return ans;
}
```

 Example:

```
n = 6, k = 3

0 1 2 4 4 4
```

 MEX = `3`.

---

 # 17\. MEX of a permutation

 For a permutation containing:

```
0 ... n-1
```

 the MEX of the **entire array** is simply:

```
int mex = n;
```

 But for subarrays, use positions.

```
vector<int> pos(n);

for (int i = 0; i < n; i++)
    pos[a[i]] = i;
```

 Now:

```
pos[x]
```

 tells you where `x` occurs.

 For example, if you need a range containing:

```
0, 1, ..., k-1
```

 maintain:

```
int L = n;
int R = -1;

for (int x = 0; x < k; x++) {
    L = min(L, pos[x]);
    R = max(R, pos[x]);
}
```

 Then `[L,R]` is the smallest range containing all `0...k-1`.

 This is a powerful **permutation + MEX** pattern.

---

 # 18\. MEX after one replacement

 A useful generic approach:

```
int currentMex(vector<int>& a) {
    return mex(a);
}
```

 But for one replacement, don't necessarily recompute the whole array.

 Maintain:

```
vector<int> freq(n + 1);

for (int x : a)
    if (0 <= x && x <= n)
        freq[x]++;
```

 Then after replacing `oldValue` with `newValue`:

```
freq[oldValue]--;
freq[newValue]++;
```

 Recalculate MEX:

```
int mex = 0;

while (mex <= n && freq[mex] > 0)
    mex++;
```

 For many replacements, use the dynamic-MEX template instead.

---

 # 19\. MEX after arbitrary updates

 Suppose operations are:

```
update index i → x
query MEX
```

 Use:

```
vector<int> a(n);
vector<int> freq(n + 1);
set<int> missing;

for (int i = 0; i <= n; i++)
    missing.insert(i);

for (int x : a) {
    if (0 <= x && x <= n) {
        freq[x]++;
        missing.erase(x);
    }
}

auto update = [&](int idx, int x) {

    int old = a[idx];

    if (0 <= old && old <= n) {
        freq[old]--;

        if (freq[old] == 0)
            missing.insert(old);
    }

    a[idx] = x;

    if (0 <= x && x <= n) {
        freq[x]++;

        if (freq[x] == 1)
            missing.erase(x);
    }
};

auto getMex = [&]() {
    return *missing.begin();
};
```

 This handles:

```
update → O(log n)
query  → O(1)
```

---

 # 20\. MEX + XOR

 Suppose the array is transformed:

```
b[i] = a[i] ^ x;
```

 For small constraints:

```
vector<int> freq(n + 1);

for (int v : a) {
    int y = v ^ x;

    if (0 <= y && y <= n)
        freq[y]++;
}

int mex = 0;

while (freq[mex] > 0)
    mex++;
```

 But for large XOR/MEX problems, this often becomes a **binary trie** problem.

 The key transformation is:

```
Need y present
where

y = a XOR x

⇔

a = y XOR x
```

 So for each desired MEX candidate `y`, you check whether:

```
y XOR x
```

 exists.

---

 # 21\. MEX + bitwise trie

 For problems asking something like:

```
maximum/minimum XOR subject to MEX conditions
```

 you'll often build a binary trie.

 Basic insertion:

```
struct Trie {
    struct Node {
        int child[2];

        Node() {
            child[0] = child[1] = -1;
        }
    };

    vector<Node> t;

    Trie() {
        t.push_back(Node());
    }

    void insert(int x) {
        int node = 0;

        for (int b = 30; b >= 0; b--) {
            int bit = (x >> b) & 1;

            if (t[node].child[bit] == -1) {
                t[node].child[bit] = t.size();
                t.push_back(Node());
            }

            node = t[node].child[bit];
        }
    }
};
```

 The exact trie operation depends on the problem, but this is the basic structure to recognize.

---

 # 22\. MEX + prefix/suffix + split condition

 A classic pattern:

 > Find `i` such that `MEX(left) == MEX(right)`.

```
vector<int> pref(n);
vector<int> suff(n);

// prefix
{
    vector<int> freq(n + 1);
    int mex = 0;

    for (int i = 0; i < n; i++) {

        if (a[i] >= 0 && a[i] <= n)
            freq[a[i]]++;

        while (freq[mex] > 0)
            mex++;

        pref[i] = mex;
    }
}

// suffix
{
    vector<int> freq(n + 1);
    int mex = 0;

    for (int i = n - 1; i >= 0; i--) {

        if (a[i] >= 0 && a[i] <= n)
            freq[a[i]]++;

        while (freq[mex] > 0)
            mex++;

        suff[i] = mex;
    }
}

// check splits
for (int i = 0; i + 1 < n; i++) {

    if (pref[i] == suff[i + 1]) {
        cout << "valid split\n";
    }
}
```

---

 # 23\. MEX of two sets combined

 Suppose:

```
MEX(A ∪ B)
```

 You can simply combine frequencies:

```
vector<int> freq(n + 1);

for (int x : A)
    if (0 <= x && x <= n)
        freq[x]++;

for (int x : B)
    if (0 <= x && x <= n)
        freq[x]++;

int mex = 0;

while (freq[mex])
    mex++;
```

 If you only care about presence, duplicates don't matter.

---

 # 24\. MEX of multiple sets

 Same idea:

```
vector<int> freq(n + 1);

for (auto &v : arrays) {
    for (int x : v) {
        if (0 <= x && x <= n)
            freq[x] = 1;
    }
}

int mex = 0;

while (freq[mex])
    mex++;
```

---

 # 25\. MEX with coordinate compression

 Usually MEX itself **doesn't need coordinate compression**, because:

```
MEX ≤ n
```

 This is an important trick.

 If your array contains:

```
10^18, 999999999999, 5, 0
```

 and has only `n = 4` elements, you only care about:

```
0,1,2,3,4
```

 So don't compress unnecessarily.

---

 # 26\. The fastest reusable MEX template

 If you're in a contest and just need MEX:

```
int mex(const vector<int>& a) {

    int n = a.size();

    vector<int> freq(n + 1, 0);

    for (int x : a) {
        if (0 <= x && x <= n)
            freq[x]++;
    }

    for (int i = 0; i <= n; i++) {
        if (freq[i] == 0)
            return i;
    }

    return n;
}
```

---

 # 27\. The MEX template I'd actually memorize

 For most dynamic problems, memorize this:

```
struct Mex {
    int n;
    vector<int> freq;
    int mex;

    Mex(int n) : n(n), freq(n + 1, 0), mex(0) {}

    void add(int x) {
        if (x < 0 || x > n)
            return;

        freq[x]++;

        if (x == mex) {
            while (mex <= n && freq[mex] > 0)
                mex++;
        }
    }

    void remove(int x) {
        if (x < 0 || x > n)
            return;

        freq[x]--;

        if (freq[x] == 0 && x < mex)
            mex = x;
    }

    int get() {
        return mex;
    }
};
```

 Usage:

```
Mex M(n);

for (int x : a)
    M.add(x);

cout << M.get() << '\n';

M.remove(0);
M.add(10);

cout << M.get() << '\n';
```

---

 ## The 6 templates worth memorizing

 If you don't want to memorize all of the above, prioritize these:

```
1. Basic MEX
   frequency[] + scan

2. Dynamic MEX
   frequency[] + current mex

3. Sliding-window MEX
   add() + remove() + current mex

4. Prefix/Suffix MEX
   prefixMex[] + suffixMex[]

5. MEX = K
   0..K-1 present AND K absent

6. Permutation + MEX
   positions of 0,1,...,K-1
```

 Those six patterns cover a **large fraction of the MEX problems you'll encounter**.