## Biweekly Contest 3 Solution

本周比赛比较简单，考察内容比较实用，用到的方法有滑动窗口、排序和并查集。

### [1099. 小于 K 的两数之和](https://leetcode-cn.com/contest/biweekly-contest-3/problems/two-sum-less-than-k/)

给你一个整数数组 `A` 和一个整数 `K`，请在该数组中找出两个元素，使它们的和小于 `K` 但尽可能地接近 `K`，**返回这两个元素的和**。

如不存在这样的两个元素，请返回 `-1`。

**示例 1：**

```
输入：A = [34,23,1,24,75,33,54,8], K = 60
输出：58
解释：
34 和 24 相加得到 58，58 小于 60，满足题意。
```

**示例 2：**

```
输入：A = [10,20,30], K = 15
输出：-1
解释：
我们无法找到和小于 15 的两个元素。
```

**提示：**

1. `1 <= A.length <= 100`
2. `1 <= A[i] <= 1000`
3. `1 <= K <= 2000`

**思路：**

由于数组的长度范围只有`100`，所以暴力枚举即可。每次枚举数组中两个不同的数，先判断这两个数的和是否小于`K`：如果大于等于`K`，则跳过；如果小于`K`，则继续比较和`K`的差值是否小于当前答案，如果差值更小，则更新答案。设初始答案为`ans = -1`，程序结束返回`ans`即可。

**代码：**

```python
class Solution:
    def twoSumLessThanK(self, A: List[int], K: int) -> int:
        n = len(A)
        ans = -1
        for i in range(n - 1):
            for j in range(i + 1, n):
                if A[i] + A[j] < K and K - A[i] - A[j] < K - ans:
                    ans = A[i] + A[j]
        return ans
```

### [1100. 长度为 K 的无重复字符子串](https://leetcode-cn.com/contest/biweekly-contest-3/problems/find-k-length-substrings-with-no-repeated-characters/)

给你一个字符串 `S`，找出所有长度为 `K` 且不含重复字符的子串，请你返回全部满足要求的子串的 **数目**。

**示例 1：**

```
输入：S = "havefunonleetcode", K = 5
输出：6
解释：
这里有 6 个满足题意的子串，分别是：'havef','avefu','vefun','efuno','etcod','tcode'。
```

**示例 2：**

```
输入：S = "home", K = 5
输出：0
解释：
注意：K 可能会大于 S 的长度。在这种情况下，就无法找到任何长度为 K 的子串。
```

**提示：**

1. `1 <= S.length <= 10^4`
2. `S` 中的所有字符均为小写英文字母
3. `1 <= K <= 10^4`

**思路：**

本题与[3. 无重复字符的最长子串](https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/)采用算法相似，都是滑动窗口。先判断字符串长度是否小于`K`，如果小于`K`则直接返回`0`。如果不小于`K`，则维护一个长度为`K`的滑动窗口，用哈希字典来存储窗口中每个字符在字符串中出现的位置。每次读进一个字符：如果已经在字典中出现，那么从字典中取出这个字符的索引，将滑动窗口内的索引前字符全部从字典中删除；如果字符未在字典中出现，那么把字符加入字典，同时窗口向右滑动。

**代码：**

```python
class Solution:
    def numKLenSubstrNoRepeats(self, S: str, K: int) -> int:
        n = len(S)
        ans = 0
        if n < K:
            return 0
        d = dict()
        length = 0
        for i in range(n):
            if S[i] in d:
                last = d[S[i]]
                for j in range(i - length, last + 1):
                    del d[S[j]]
                length = i - last
            else:
                length += 1
            d[S[i]] = i
            if length > K:
                length -= 1
                del d[S[i - length]]
            if length == K:
                ans += 1
        return ans
```

### [1101. 彼此熟识的最早时间](https://leetcode-cn.com/contest/weekly-contest-143/problems/filling-bookcase-shelves/)

在一个社交圈子当中，有 `N` 个人。每个人都有一个从 `0` 到 `N-1` 唯一的 id 编号。

我们有一份日志列表 `logs`，其中每条记录都包含一个非负整数的时间戳，以及分属两个人的不同 id，`logs[i] = [timestamp, id_A, id_B]`。

每条日志标识出两个人成为好友的时间，友谊是相互的：如果 A 和 B 是好友，那么 B 和 A 也是好友。

如果 A 是 B 的好友，或者 A 是 B 的好友的好友，那么就可以认为 A 也与 B 熟识。

返回圈子里所有人之间都熟识的最早时间。如果找不到最早时间，就返回 `-1` 。

**示例：**

```
输入：logs = [[20190101,0,1],[20190104,3,4],[20190107,2,3],[20190211,1,5],[20190224,2,4],[20190301,0,3],[20190312,1,2],[20190322,4,5]], N = 6
输出：20190301
解释：
第一次结交发生在 timestamp = 20190101，0 和 1 成为好友，社交朋友圈如下 [0,1], [2], [3], [4], [5]。
第二次结交发生在 timestamp = 20190104，3 和 4 成为好友，社交朋友圈如下 [0,1], [2], [3,4], [5].
第三次结交发生在 timestamp = 20190107，2 和 3 成为好友，社交朋友圈如下 [0,1], [2,3,4], [5].
第四次结交发生在 timestamp = 20190211，1 和 5 成为好友，社交朋友圈如下 [0,1,5], [2,3,4].
第五次结交发生在 timestamp = 20190224，2 和 4 已经是好友了。
第六次结交发生在 timestamp = 20190301，0 和 3 成为好友，大家都互相熟识了。
```

**提示：**

1. `1 <= N <= 100`
2. `1 <= logs.length <= 10^4`
3. `0 <= logs[i][0] <= 10^9`
4. `0 <= logs[i][1], logs[i][2] <= N - 1`
5. 保证 `logs[i][0]` 中的所有时间戳都不同
6. `Logs` 不一定按某一标准排序
7. `logs[i][1] != logs[i][2]`

**思路：**

由于题目要求返回圈子里所有人之间都熟识的最早时间，所以首先要把`logs`按照时间顺序排序。本题的实质是在一个无向图中，有`N`个结点，每个`log`是连通两个结点的一条边，求按照时间顺序在图中加边，最早什么时候能把整个图合成一个连通分量。关于连通分量，可以用并查集来解决，自己写一个并查集类，记录每个结点的父结点，和该结点连通分量的大小。每次读入一个`log`，把`log`中两个结点所属集合合并，然后检测一下合并之后的集合大小是不是等于`N`，即所有人之间都熟识，如果等于`N`，则直接返回该`log`的时间。

**代码：**

```python
class DSU(object):
    def __init__(self, n):
        self.par = [i for i in range(n)]
        self.sz = [1] * n

    def find(self, x):
        if self.par[x] != x:
            self.par[x] = self.find(self.par[x])
        return self.par[x]

    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return
        if self.sz[xr] < self.sz[yr]:
            xr, yr = yr, xr
        self.par[yr] = xr
        self.sz[xr] += self.sz[yr]


class Solution:
    def earliestAcq(self, logs: List[List[int]], N: int) -> int:
        dsu = DSU(N)
        logs.sort()
        for log in logs:
            a = log[1]
            b = log[2]
            dsu.union(a, b)
            if dsu.sz[dsu.find(a)] == N:
                return log[0]
        return -1
```

### [1102. 得分最高的路径](https://leetcode-cn.com/contest/biweekly-contest-3/problems/path-with-maximum-minimum-value/)

给你一个 R 行 C 列的整数矩阵 `A`。矩阵上的路径从 `[0,0]` 开始，在 `[R-1,C-1]` 结束。

路径沿四个基本方向（上、下、左、右）展开，从一个已访问单元格移动到任一相邻的未访问单元格。

路径的得分是该路径上的 **最小** 值。例如，路径 8 →  4 →  5 →  9 的值为 4 。

找出所有路径中得分 **最高** 的那条路径，返回其 **得分**。

**示例 1：**

**![img](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2019/06/27/1313_ex1.jpeg)**

```
输入：[[5,4,5],[1,2,6],[7,4,6]]
输出：4
解释： 
得分最高的路径用黄色突出显示。 
```

**示例 2：**

**![img](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2019/06/27/1313_ex2.jpeg)**

```
输入：[[2,2,1,2,2,2],[1,2,2,2,1,2]]
输出：2
```

**示例 3：**

**![img](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2019/06/27/1313_ex3.jpeg)**

```
输入：[[3,4,6,3,4],[0,2,1,1,7],[8,8,3,2,7],[3,2,4,9,8],[4,1,2,0,0],[4,6,5,4,3]]
输出：3
```

**提示：**

1. `1 <= R, C <= 100`
2. `0 <= A[i][j] <= 10^9`

**思路：**

本题有多种方法，比如DP或二分DFS。本题解采用与周赛第三题[彼此熟识的最早时间](https://leetcode-cn.com/contest/biweekly-contest-3/problems/the-earliest-moment-when-everyone-become-friends/)同样的方法，排序加并查集。初始答案`ans`是第一个格子和最后一个格子两者之间的最小值`min(A[0][0], A[R - 1][C - 1])`，先将所有格子按照`(数值, 行, 列)`组成的三元组，加进一个`list`里面，然后对这个`list`进行排序。按照格子值从大到小进行遍历，没读取一个格子，就把格子进行染色，用集合`s`来表示已经染色的格子集合，然后检查该格子的上下左右是否也经过染色，如果也染过色，那么将该格子加入到同一个并查集里。直到第一个格子和最后一个格子属于同一个并查集，遍历结束。在遍历过程中不断更新`ans`，遍历结束后返回`ans`即可。

**代码：**

```python
class DSU(object):
    def __init__(self, n):
        self.par = [i for i in range(n)]
        self.sz = [1] * n

    def find(self, x):
        if self.par[x] != x:
            self.par[x] = self.find(self.par[x])
        return self.par[x]

    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return
        if self.sz[xr] < self.sz[yr]:
            xr, yr = yr, xr
        self.par[yr] = xr
        self.sz[xr] += self.sz[yr]

class Solution:
    def maximumMinimumPath(self, A: List[List[int]]) -> int:
        R = len(A)
        C = len(A[0])
        n = R * C
        d = DSU(n)
        s = set()
        points = []
        for i in range(R):
            for j in range(C):
                points.append((A[i][j], i, j))
        points.sort()
        ans = min(A[0][0], A[R - 1][C - 1])
        s.add((0, 0))
        s.add((R - 1, C - 1))
        while d.find(0) != d.find(n - 1):
            p, x, y = points.pop()
            ans = min(ans, p)
            for i, j in [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]:
                if (i, j) in s:
                    d.union(x * C + y, i * C + j)
                s.add((x, y))
        return ans
```