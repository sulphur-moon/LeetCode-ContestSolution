## [第 146 场周赛](https://leetcode-cn.com/contest/weekly-contest-146)

本周比赛题目比较难，与上周周赛一样，考察重点是对题目的理解和编程技巧，其中第三题多种解法，想要在比赛中写出最优解法比较困难。本周比赛用到的算法有排序、广度优先搜索、动态规划、单调栈等等。

### [1128. 等价多米诺骨牌对的数量](https://leetcode-cn.com/contest/weekly-contest-146/problems/number-of-equivalent-domino-pairs)

**思路：**

把每个多米诺骨牌翻成小的数字在上，大的数字在下的情况，这样可以使相同的多米诺骨牌的状态也相同，便于统计数目。然后用哈希字典来统计每种多米诺骨牌的个数，最后遍历每种骨牌，用组合数学 `n * (n - 1) // 2` 求每种骨牌成对的数目，将其累加得到最后结果。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1128-1.gif)


**代码：**
```python
class Solution:
    def numEquivDominoPairs(self, dominoes: List[List[int]]) -> int:
        ans = 0
        d = dict()
        for d1, d2 in dominoes:
            # 排序后加入字典
            index = tuple(sorted((d1, d2)))
            if index in d:
                d[index] += 1
            else:
                d[index] = 1
        # 计算答案
        for i in d:
            ans += d[i] * (d[i] - 1) // 2
        return ans
```


### [1129. 颜色交替的最短路径](https://leetcode-cn.com/contest/weekly-contest-146/problems/shortest-path-with-alternating-colors)

**思路：**

这道题的难点在于理解题意和编写代码。要求所有最短路径的长度，我们很容易想到广度优先搜索。问题是，从结点 0 出发，可以先走红色边，也可以先走蓝色边。我们当然可以先走红色边 BFS 一遍，再先走蓝色边 BFS 一遍。但是这样代码写两份就比较冗长。所以，我们需要在队列里加入结点的时候，设计一个变量，表示下一步是该走红色边还是该走蓝色边。我这里用 `True` 来表示下一步该走红色边，用 `False` 来表示下一步该走蓝色边。所以搜索队列的初始状态是 `[(0, True), (0, False)]` 。那么，将结点取出时，我们就可以判断第二个变量值来选择从哪个类型的边进行搜索。


**代码：**
```python
class Solution:
    def shortestAlternatingPaths(self, n: int, red_edges: List[List[int]], blue_edges: List[List[int]]) -> List[int]:
        # 答案数组
        ans = [-1] * n
        ans[0] = 0
        # 访问过的结点
        visited = set()
        visited.add((0, True))
        visited.add((0, False))
        # 初始结点
        q = [(0, True), (0, False)]
        # 红色边和蓝色边
        r = collections.defaultdict(set)
        b = collections.defaultdict(set)
        for e in red_edges:
            r[e[0]].add(e[1])
        for e in blue_edges:
            b[e[0]].add(e[1])
        # 步数
        step = 0
        # BFS
        while q:
            step += 1
            t = []
            while q:
                node, color = q.pop()
                if color and node in r:
                    for next_node in r[node]:
                        if (next_node, False) not in visited:
                            visited.add((next_node, False))
                            if ans[next_node] == -1:
                                ans[next_node] = step
                            t.append((next_node, False))
                elif not color and node in b:
                    for next_node in b[node]:
                        if (next_node, True) not in visited:
                            if ans[next_node] == -1:
                                ans[next_node] = step
                            t.append((next_node, True))
            q = t
        return ans
```


### [1130. 叶值的最小代价生成树](https://leetcode-cn.com/contest/weekly-contest-146/problems/minimum-cost-tree-from-leaf-values)

**思路：**

这道题比较容易想到的解法是一个 $O(N^3)$ 的动态规划解法。我们用 `dp[i][j]` 来表示用子数组 `arr[i:j+1]` （即数组中第 i 个元素到第 j 个元素，编号从 0 开始）构成树的最小代价，那么我们可以写出状态转移方程为：

$$dp_{ij} = min_{1 <= k < j}(dp_{ik} + dp_{kj} + max(arr[i:k]) * max(arr[k+1:j])) $$

那么，最终我们要求的结果就是 `dp[0][n - 1]`  的值。枚举过程是先枚举区间长度 `l`，再枚举起始点 `s`，根据起始点和长度算出区间终点 `s + l`，最后枚举区间中的点 `k`。

但是这道题目有更简单的解法。下面简述一下来自于 [lee215](https://leetcode.com/lee215/) 的思路，时间复杂度为 $O(N)$ 。这道题可以看做如下过程：在数组 `arr` 中，每次取相邻的两个数 `a` 和 `b`，然后去掉其中较小的一个，花费代价为 `a * b`，求最终将数组消减为一个元素的最小代价。那么，要想获得最小代价，我们应该采取的策略是：对于数组中的某一个数 `a`，分别向左和向右查询比它大的第一个数，在这两个数中选择较小的那个数把它消去，花费的代价最小。这个过程我们可以用单调栈来一次遍历解决掉。


**代码：**

动态规划：

```python
class Solution:
    def mctFromLeafValues(self, arr: List[int]) -> int:
        n = len(arr)
        # 初始值设为最大
        dp = [[float('inf') for _ in range(n)] for _ in range(n)]
        # 初始区间查询最大值设为0
        maxval = [[0 for _ in range(n)] for _ in range(n)]
        # 求区间[i, j]中最大元素
        for i in range(n):
            for j in range(i, n):
                maxval[i][j] = max(arr[i:j + 1])
        # 叶子结点不参与计算
        for i in range(n):
            dp[i][i] = 0
        # 枚举区间长度
        for l in range(1, n):
            # 枚举区间起始点
            for s in range(n - l):
                # 枚举划分两棵子树
                for k in range(s, s + l):
                    dp[s][s + l] = min(dp[s][s + l], dp[s][k] + dp[k + 1][s + l] + maxval[s][k] * maxval[k + 1][s + l])
        return dp[0][n - 1]
```

单调栈：

```python
class Solution:
    def mctFromLeafValues(self, A: List[int]) -> int:
        res, n = 0, len(A)
        stack = [float('inf')]
        for a in A:
            while stack[-1] <= a:
                mid = stack.pop()
                res += mid * min(stack[-1], a)
            stack.append(a)
        while len(stack) > 2:
            res += stack.pop() * stack[-1]
        return res
```


### [1131. 绝对值表达式的最大值](https://leetcode-cn.com/contest/weekly-contest-146/problems/maximum-of-absolute-value-expression)

**思路：**

我们将 `arr1` 中的所有值看做平面上点的横坐标，将` arr2` 中的所有值看做平面上点的纵坐标，那么表达式`|arr1[i] - arr1[j]| + |arr2[i] - arr2[j]| + |i - j|` 前两项就可以看成是平面上两点的曼哈顿距离，整个式子就是要求两个点的曼哈顿距离与两个点索引差的和。

由于有取绝对值的操作存在，那么可能产生的计算有 4 种，分别为：右上减左下，右下减左上，左上减右下，左下减右上。以测试样例为例，第一组样例如左图，右上减左下取得最大值为 `3 + 7 + 3 = 13`；第二组样例如右图，右下减左上取得最大值为 `15 + 3 + 2 = 20`。

![图解](http://qiniu.wenyuetech.cn/1131-1.png)

所以我们枚举 4 种情况，分别求出每种情况中的最大值和最小值，然后做差更新答案即可。


**代码：**
```python
class Solution:
    def maxAbsValExpr(self, arr1: List[int], arr2: List[int]) -> int:
        n = len(arr1)
        ans = 0
        # 枚举四个方向
        for dx, dy in [(1, 1), (-1, 1), (1, -1), (-1, -1)]:
            maxv = 0
            minv = 4000000
            # 计算当前方向上的曼哈顿距离最小值和最大值
            for i in range(n):
                maxv = max(maxv, arr1[i] * dx + arr2[i] * dy + i)
                minv = min(minv, arr1[i] * dx + arr2[i] * dy + i)
            # 更新答案
            ans = max(ans, maxv - minv)
        return ans
```


