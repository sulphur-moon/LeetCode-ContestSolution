## [第 107 场周赛](https://leetcode-cn.com/contest/weekly-contest-107)

本周比赛难度适中，用到了数学、并查集、广度优先搜索等算法。

### [925. 长按键入](https://leetcode-cn.com/contest/weekly-contest-107/problems/long-pressed-name)

**思路：**

1. 两个指针分别指向 `name` 和 `typed`，如果字符相等，就都右移一；
2. 如果不等，检查 `typed` 中字符是否重复，如果不重复直接返回 `False`，如果重复就一直指针一直右移到不重复为止；
3. 重复前两个步骤直到其中一个指针遍历完成，如果 `name` 未遍历完成而 `typed` 遍历完成了，那么返回`False`，如果 `typed` 未遍历完成而 `name` 遍历完成了，那么要判断是否`typed`后面多余的字符都是 `name` 的最后一个字符，是则返回 `True`，否则返回 `False`。

时间复杂度 $O(N)$

空间复杂度 $O(1)$


**代码：**
```python
class Solution:
    def isLongPressedName(self, name: str, typed: str) -> bool:
        p1 = 0
        p2 = 0
        while p1 < len(name) and p2 < len(typed):
            if name[p1] == typed[p2]:
                p1 += 1
                p2 += 1
            elif p2 > 0 and typed[p2] == typed[p2 - 1]:
                p2 += 1
            else:
                return False
        if p1 < len(name):
            return False
        while p2 < len(typed):
            if typed[p2] != typed[p2 - 1]:
                return False
            p2 += 1
        return True
```


### [926. 将字符串翻转到单调递增](https://leetcode-cn.com/contest/weekly-contest-107/problems/flip-string-to-monotone-increasing)

**思路：**

本题有多种思路

1. 用 `cnt0[i]` 表示第 `i` 位（包含）之前有多少个 `0`，那么我们只需要寻找一个分割点 `i`，让 `i` 之前的 `1` 和 `i` 之后的 `0` 数目之和最小。
2. 从头遍历，从第一个 `1` 开始 `0` 的数目和 `1` 的数目赛跑，每次 `0` 的数目超过 `1` 的数目翻转前面的所有 `1`，再找到下一个 `1` 从新计数，以此类推。最后`0`的数目不超过`1`的数目翻转后面剩下的`0`。程序中只需要计数，不需要真实的翻转。
3. 某一位为 `1` 时，前面一位是 `0` 或者 `1` 都可以；某一位为 `0` 时，前面一位只能为 `0`。
4. 用 `one` 表示到第 `i` 位为止 `1` 的个数，用 `d` 表示 `1` 的个数减去 `0` 的个数，遍历时维护 `d` 的最小值，即可得到结果为 `d + len(S) - one`。

时间复杂度 $O(N)$

空间复杂度 $O(N)$


**代码：**

解法1：

```python
class Solution:
    def minFlipsMonoIncr(self, S: str) -> int:
        l = len(S)
        cnt0 = [0] * (l + 1)
        for i in range(l):
            cnt0[i + 1] = cnt0[i]
            if S[i] == "0":
                cnt0[i + 1] += 1
        ans = l - cnt0[l]
        for i in range(l):
            ans = min(ans, i - cnt0[i] + cnt0[l] - cnt0[i])
        return ans
```

解法2：

```python
class Solution:
    def minFlipsMonoIncr(self, S: str) -> int:
        p, ans, zero, one = 0, 0, 0, 0
        while p < len(S):
            if S[p] == '1':
                one += 1
            elif one > 0:
                zero += 1
            if zero > one:
                ans += one
                zero, one = 0, 0
            p += 1
        return ans + zero
```

解法3：

```python
class Solution:
    def minFlipsMonoIncr(self, S: str) -> int:
        zero, one = 0, 0
        for i in S:
            if i == '1':
                one = min(zero, one)
                zero += 1
            else:
                one = min(zero, one) + 1
        return min(zero, one)
```

解法4：

```python
class Solution:
    def minFlipsMonoIncr(self, S: str) -> int:
        one, d = 0, 0
        for i in range(0, len(S)):
            if S[i] == '1':
                one += 1
            elif d > one - (i + 1 - one):
                d = one - (i + 1 - one)
        return d + len(S) - one
```
### [927. 三等分](https://leetcode-cn.com/contest/weekly-contest-107/problems/three-equal-parts)

**思路：**

直接模拟判断：首先统计 `1` 的个数，如果 `1` 的个数不是 `3` 的倍数，那么直接返回无解；如果数组中没有 `1`，那么直接返回 `[0, 2]`。否则按照 `1` 的个数来划分数组，判断表示的二进制是否相等，注意最后一个数有多少个结尾 `0`。

时间复杂度 $O(N)$

空间复杂度 $O(N)$


**代码：**

```python
class Solution:
    def threeEqualParts(self, A: List[int]) -> List[int]:
        
        def check(A1, A2, A3):
            if not len(A1) == len(A2) == len(A3):
                return False
            for i in range(len(A1)):
                if not A1[i] == A2[i] == A2[i]:
                    return False
            return True
        
        cnt1 = 0
        for i in A:
            if i == 1:
                cnt1 += 1
        if cnt1 == 0:
            return [0, 2]
        if cnt1 % 3 != 0:
            return [-1, -1]
        interval = [[0, 0], [0, 0], [0, 0]]
        cnt = 0
        j = 0
        for i in range(len(A)):
            if A[i] == 1:
                if cnt == 0:
                    interval[j][0] = i
                cnt += 1
                if cnt == cnt1 // 3:
                    interval[j][1] = i + 1
                    j += 1
                    cnt = 0
        if check(A[interval[0][0]:interval[0][1]], A[interval[1][0]:interval[1][1]], A[interval[2][0]:interval[2][1]]):
            zero_last = len(A) - interval[2][1]
            if interval[1][0] - interval[0][1] >= zero_last and interval[2][0] - interval[1][1] >= zero_last:
                return [interval[0][1] - 1 + zero_last, interval[1][1] + zero_last]
            else:
                return [-1, -1]
        else:
            return [-1, -1]
```

更简单的写法：

```python
class Solution:
    def threeEqualParts(self, A: List[int]) -> List[int]:
        N = len(A)
        pos = [i for i in range(N) if A[i] == 1]
        if not pos:return [0, N-1]
        rd1, rd2, rd3 = pos[0], pos[len(pos)//3], pos[len(pos)//3*2]
        sub = N - rd3
        if len(pos)%3 == 0 and A[rd1:rd1+sub] == A[rd2:rd2+sub] == A[rd3:]:
            return [rd1+sub-1,rd2+sub]
        return [-1, -1]
```


### [928. 尽量减少恶意软件的传播 II](https://leetcode-cn.com/contest/weekly-contest-107/problems/minimize-malware-spread-ii)

**思路：**

根据题意直接进行 `initial.length` 遍BFS统计病毒感染数，最少的即为答案。BFS时，需要剔除第 `i` 个结点，直接先把它标记为被访问过即可。

时间复杂度 $O(NM)$

空间复杂度 $O(N)$


**代码：**
```python
class Solution:
    def minMalwareSpread(self, graph: List[List[int]], initial: List[int]) -> int:
        
        def bfs(g, init, i):
            ret = 0
            n = len(g)
            visited = [False] * n
            visited[init[i]] = True
            q = []
            for j in range(len(init)):
                if j != i:
                    q.append(init[j])
                    visited[init[j]] = True
            while q:
                t = []
                while q:
                    node = q.pop()
                    for j in range(n):
                        if not visited[j] and g[node][j]:
                            t.append(j)
                            visited[j] = True
                            ret += 1
                q = t
            return ret
        
        initial.sort()
        ans = initial[0]
        m = bfs(graph, initial, 0)
        for i in range(1, len(initial)):
            t = bfs(graph, initial, i)
            if t < m:
                m = t
                ans = initial[i]

        return ans
```
