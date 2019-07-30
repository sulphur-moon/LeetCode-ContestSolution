## [第 5 场双周赛](https://leetcode-cn.com/contest/biweekly-contest-5)

本场双周赛比较简单，用到算法有统计、数学、最小生成树、拓扑排序等。其中，后两道图论算法可以说是裸题，第三题重点考察根据数据规模选择Prim算法还是Kruskal算法，第四题考察的是记录拓扑排序的层次，对于图论算法不太熟悉的同学可能有些难度。

### [1133. 最大唯一数](https://leetcode-cn.com/contest/biweekly-contest-5/problems/largest-unique-number)

**思路：**

直接统计所有元素出现的次数，然后将元素从大到小排序，从最大元素开始检查是否唯一：如果不唯一则跳过，直到检查到唯一的元素为止，返回这个元素；如果所有元素都不唯一，那么返回 -1。


**代码：**
```python
class Solution:
    def largestUniqueNumber(self, A: List[int]) -> int:
        c = collections.Counter(A)
        for i in sorted(c.keys(), reverse=True):
            if c[i] == 1:
                return i
        return -1
```


### [1134. 阿姆斯特朗数](https://leetcode-cn.com/contest/biweekly-contest-5/problems/armstrong-number)

**思路：**

把 N 的每一位都放进一个数组里，则 k 为数组长度，然后将每一位的 k 次方加和，判断结果是否和原来的 N 相等。


**代码：**
```python
class Solution:
    def isArmstrong(self, N: int) -> bool:
        origin = N
        nums = []
        while N > 0:
            nums.append(N % 10)
            N //= 10
        k = len(nums)
        s = 0
        for n in nums:
            s += n ** k
        return s == origin
```


### [1135. 最低成本联通所有城市](https://leetcode-cn.com/contest/biweekly-contest-5/problems/connecting-cities-with-minimum-cost)

**思路：**

本题考查的是最小生成树，一个有 n 个结点的连通图的生成树是原图的极小连通子图，且包含原图中的所有 n 个结点，并且有保持图连通的最少的边。最小生成树可以用克鲁斯卡尔（Kruskal）算法或普里姆（Prim）算法求出。设原图中结点数目为 V，边数为 E，那么 Kruskal 算法的时间复杂度为 $O(Elog(E))$，而 Prim 算法的时间复杂度为 $O(V^2)$，虽然使用二叉堆优化 Prim 算法的时间复杂度为 $O((V + E) log(V)) = O(E log(V))$，或者进一步用斐波那契堆可以优化至 $O(E + V log(V))$，但是编程的复杂度会变得非常高。 所以本题还是采用并查集优化的 Kruskal 算法最为合适。具体过程如下：

1. 将 `connections` 按照权值排序，并初始化一个规模为 `N` 的并查集；
2. 用 `ans` 表示最终花费，用 `cnt` 表示已经采用的边的个数；
3. 按照从小到大的顺序在 `connections` 里面取边，如果这条边连接的两个结点已经在同一个连通分量里（用并查集查询），那么忽略这条边；如果两个结点不连通，那么将这条边计入 `ans`，并且合并这条边连接的两个连通分量；
4. 如果 `cnt` 计数已经到达 `N - 1`，说明已经形成了最小生成树，直接返回 `ans`；
5. 如果 `connections` 遍历完，`cnt` 也没有达到 `N - 1`，说明最小生成树不存在，返回 `-1`。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1135-1.gif)


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
    def minimumCost(self, N: int, connections: List[List[int]]) -> int:
        en = len(connections)
        if en < N - 1:
            return -1
        # 边按权值排序
        connections.sort(key=lambda x:x[2])
        ans, cnt = 0, 0
        # 并查集检查连通性
        dsu = DSU(N)
        for x, y, w in connections:
            # 如果两端点不连通，则将这条边加入
            if dsu.find(x - 1) != dsu.find(y - 1):
                ans += w
                cnt += 1
                # 如果加到 N - 1 条边，就满足最小生成树
                if cnt == N - 1:
                    return ans
                dsu.union(x - 1, y - 1)
        return -1
```


### [1136. 平行课程](https://leetcode-cn.com/contest/biweekly-contest-5/problems/parallel-courses)

**思路：**

这是一道拓扑排序题，标准拓扑排序的过程为：

1. 选择一个入度为 0 的顶点并输出之；
2. 从网中删除此顶点及所有出边；
3. 重复 1、2 两步，直到不存在入度为 0 的顶点为止；
4. 循环结束后，若输出的顶点数小于网中的顶点数，则图中有回路存在，否则，输出序列为其中一种拓扑排序方式。

求最少学期数可以采用贪心的方式，每个学期，把所有先修课程修完的课程都学完，这样可以保证每个课程都尽量提前学到，那么总体上所用的学期数也是最少的。求少步骤的贪心过程一般用广度优先搜索（BFS）来解决，过程如下：

1. 先统计一下每个点的入度和所有出边；
2. 选择所有入度为 0 的结点并加入队列；
3. 遍历队列中所有结点并删掉结点的出边；
4. 学期数加 1，并跳转至步骤 2 继续循环搜索，直到没有新结点能够加入到队列中；
5. 如果学习的课程已经达到 N，那么输出学期数，否则输出 -1。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1136-1.gif)


**代码：**
```python
class Solution:
    def minimumSemesters(self, N: int, relations: List[List[int]]) -> int:
        # 可以直接学习的课程集合，先把课程全部加入
        s_learned = set()
        for i in range(N):
            s_learned.add(i + 1)
        # d[i]是一个list，表示i的后继课程
        d = dict()
        # c[i]表示课程i的前置课程数目
        c = dict()
        # 计算d[i]和c[i]
        for pre, nxt in relations:
            # 如果课程有前置，那么将其移出可以直接学习的课程集合
            if nxt in s_learned:
                s_learned.remove(nxt)
            if nxt in c:
                c[nxt] += 1
            else:
                c[nxt] = 1
            if pre in d:
                d[pre].append(nxt)
            else:
                d[pre] = [nxt]
        ans = 0
        cnt = len(s_learned)
        # BFS求拓扑排序
        while s_learned:
            t = set()
            for i in s_learned:
                if i in d:
                    # 将课程i的后继课程j的入度减1
                    for j in d[i]:
                        c[j] -= 1
                        # 如果前置课程都学完了，那么加入队列
                        if c[j] == 0:
                            t.add(j)
                            del c[j]
            s_learned = t
            ans += 1
            cnt += len(t)
        return ans if cnt == N else -1
```


