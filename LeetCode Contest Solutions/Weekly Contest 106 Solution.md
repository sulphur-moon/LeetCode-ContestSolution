## [第 106 场周赛](https://leetcode-cn.com/contest/weekly-contest-106)

本周比赛比较有难度，用到了数组双指针遍历、栈、数学统计、并查集与连通分量等算法。

### [922. 按奇偶排序数组 II](https://leetcode-cn.com/contest/weekly-contest-106/problems/sort-array-by-parity-ii)

**思路：**

开一个 `ans` 数组，双指针遍历，`p1` 代表偶数指针，初始指向 `ans[0]`，`p2` 代表奇数指针，初始指向 `ans[1]`。遍历数组 `A`，如果是偶数就写入 `p1` 指针所在位置，并将 `p1` 指针加 `2`，否则就写入 `p2` 指针位置，并将 `p2` 加 `2`。

时间复杂度 $O(N)$

空间复杂度 $O(N)$


**代码：**
```python
class Solution:
    def sortArrayByParityII(self, A: List[int]) -> List[int]:
        l = len(A)
        ans = [0] * l
        p1 = 0
        p2 = 1
        for i in A:
            if i % 2 == 0:
                ans[p1] = i
                p1 += 2
            else:
                ans[p2] = i
                p2 += 2
        return ans
```


### [921. 使括号有效的最少添加](https://leetcode-cn.com/contest/weekly-contest-106/problems/minimum-add-to-make-parentheses-valid)

**思路：**

与判断括号是否合法算法一样，利用栈结构，左括号入栈，遇到右括号出栈，只不过是在判断过程中，如果非法（栈空）就补充一个左括号继续判断，结束后，如果栈非空，还要补充同样多数量的右括号，一共补充括号的数量就是答案。

时间复杂度 $O(N)$

空间复杂度 $O(N)$


**代码：**
```python
class Solution:
    def minAddToMakeValid(self, S: str) -> int:
        s = []
        ans = 0
        for i in S:
            if i == "(":
                s.append(i)
            else:
                if not s:
                    ans += 1
                else:
                    s.pop()
        ans += len(s)
        return ans
```


### [923. 三数之和的多种可能](https://leetcode-cn.com/contest/weekly-contest-106/problems/3sum-with-multiplicity)

**思路：**

先将数组 `A` 去重复，然后枚举三数之和可能的组合 `(i,j,k)` 满足 `i<=j<=k`，最后用计数算这种组合对答案有多少贡献，累加得到答案。

时间复杂度 $O(N^2)$

空间复杂度 $O(N)$


**代码：**
```python
class Solution:
    def threeSumMulti(self, A: List[int], target: int) -> int:
        mod = 1000000007
        cnt = collections.Counter(A)
        ans = 0
        for i in range(min(101, target + 1)):
            for j in range(i, target - i + 1):
                k = target - i - j
                cur = 0
                if k < j:
                    break
                if k > 100:
                    continue
                if i == j and j == k:
                    cur = (cnt[i]) * (cnt[j] - 1) * (cnt[k] - 2) // 6 % mod;
                elif i == j and j != k:
                    cur = (cnt[i]) * (cnt[j] - 1) // 2 * cnt[k] % mod;
                elif i != j and j == k:
                    cur = (cnt[i]) * cnt[j] * (cnt[k] - 1) // 2 % mod;
                else:
                    cur = (cnt[i]) * cnt[j] * cnt[k] % mod;
                ans = (ans + cur) % mod;
        return ans
```


### [924. 尽量减少恶意软件的传播](https://leetcode-cn.com/contest/weekly-contest-106/problems/minimize-malware-spread)

**思路：**

先用并查集求图的连通分量个数，再统计每个连通分量有多少个结点，然后求病毒所在连通分量，如果多个病毒在一个连通分量，那么删除其中任意一个病毒都不会使染毒结点减少，只有删除独占连通分量的病毒才有意义。那么遍历独占连通分量的病毒，看哪个独占连通分量的病毒影响结点数最多，即得出答案。

时间复杂度 $O(N^2)$

空间复杂度 $O(N)$


**代码：**
```python
class Solution:
    def minMalwareSpread(self, graph: List[List[int]], initial: List[int]) -> int:
        n = len(graph)
        # 并查集
        father = [i for i in range(n)]
        
        def get_father(i):
            if father[i] == i:
                return i
            else:
                father[i] = get_father(father[i])
                return father[i]
        
        for i in range(n - 1):
            for j in range(i + 1, n):
                if graph[i][j]:
                    fi = get_father(i)
                    fj = get_father(j)
                    if fi != fj:
                        father[fj] = fi
        # 初始结点从小到大排序
        initial.sort()
        v_n = len(initial)
        
        num = [0] * n
        # 统计连通分量大小
        for i in range(n):
            num[get_father(i)] += 1
        # 求每个病毒结点属于哪个连通分量
        v_fa = [0] * v_n
        for i in range(v_n):
            v_fa[i] = get_father(initial[i])
        # 如果多个病毒属于一个连通分量，那么删除哪个都不会使最终结果减小
        cnt = collections.Counter(v_fa)
        m = 0
        ans = initial[0]
        for i in range(v_n):
            # 只有删除独占一个连通分量的病毒才有意义
            if cnt[v_fa[i]] == 1 and num[v_fa[i]] > m:
                ans = initial[i]
                m = num[v_fa[i]]
        return ans
```


