## [第 155 场周赛](https://leetcode-cn.com/contest/weekly-contest-155)

本周比赛考察了排序、容斥原理、二分、并查集、连通分量、拓扑排序等算法。

### [1200. 最小绝对差](https://leetcode-cn.com/contest/weekly-contest-155/problems/minimum-absolute-difference)

**思路：**

最小绝对差只存在于排序后相邻的元素之间，所以先把所有元素进行排序，再进行遍历，找出最小绝对差，然后进行第二遍遍历，将满足最小绝对差的元素对输出即可。


**代码：**
```python
class Solution:
    def minimumAbsDifference(self, arr: List[int]) -> List[List[int]]:
        arr.sort()
        n = len(arr)
        m = arr[1] - arr[0]
        for i in range(1, n):
            m = min(m, arr[i] - arr[i - 1])
        ans = []
        for i in range(1, n):
            if arr[i] - arr[i - 1] == m:
                ans.append([arr[i - 1], arr[i]])
        return ans
```


### [1201. 丑数 III](https://leetcode-cn.com/contest/weekly-contest-155/problems/ugly-number-iii)

**思路：**

我们可以先求对于整数 x，在 1 ~ x 之间有多少个丑数。根据容斥原理，我们可以求出 ab、bc、ac、abc 的公倍数，然后用各自公倍数数量的和，减去两两公倍数的数量，再加上三者公倍数的数量，即得出小于等于 x 的丑数个数。最后我们用二分法来搜索答案。


**代码：**
```python
class Solution:
    def nthUglyNumber(self, n: int, a: int, b: int, c: int) -> int:
        # basic function for LCM
        def lcm(x, y):
            return (x * y) // math.gcd(x, y)

        lcm1 = lcm(a, b)
        lcm2 = lcm(b, c)
        lcm3 = lcm(c, a)
        lcm4 = lcm(lcm1, lcm2)

        # count how many ugly numbers exist below x
        def count_below(x):
            return x // a + x // b + x // c + x // lcm4 - (x // lcm1 + x // lcm2 + x // lcm3)

        # binary search
        lb = 0
        ub = 2 * 10 ** 9
        while (ub - lb > 1):
            mid = (lb + ub) // 2
            if count_below(mid) >= n:
                ub = mid
            else:
                lb = mid

        return ub
```


### [1202. 交换字符串中的元素](https://leetcode-cn.com/contest/weekly-contest-155/problems/smallest-string-with-swaps)

**思路：**

我们把字符串中的每个字符看成一个结点，每一个` pair` 看成是在结点之间的一条无向边。那么字符串就可以看成是一张有若干连通分量的图。每个连通分量中，我们可以通过若干步骤，交换任意两个结点。要想使交换之后的字符串字典序最小，那么我们在每个连通分量内，尽量让索引靠前的字符字典序也最小。

所以，我们可以用并查集求出图的所有连通分量，再按照连通分量分组进行排序，最后将排序后的字符按照索引填回字符串即可。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1202-1.png)


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
    def smallestStringWithSwaps(self, s: str, pairs: List[List[int]]) -> str:
        n = len(s)
        dsu = DSU(n)
        for p1, p2 in pairs:
            dsu.union(p1, p2)
        d = collections.defaultdict(list)
        for i in range(n):
            d[dsu.find(i)].append(i)
        ans = [''] * n
        for i, v in d.items():
            t = []
            for j in v:
                t.append(s[j])
            t.sort()
            for j in range(len(v)):
                ans[v[j]] = t[j]
        return ''.join(ans)
```


### [1203. 项目管理](https://leetcode-cn.com/contest/weekly-contest-155/problems/sort-items-by-groups-respecting-dependencies)

**思路：**

这是一个拓扑排序套拓扑排序的题目。

我们先把所有任务分组，存在字典中。然后遍历 `beforeItems`，建立组与组之间、项目与项目之间的拓扑关系。最后先对组进行拓扑排序，再对组内项目进行拓扑排序，输出答案。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1203-1.PNG)

输入样例 1 中，组间拓扑关系和组内拓扑关系均满足拓扑排序。

![图解](http://qiniu.wenyuetech.cn/1203-2.PNG)

输入样例 2 中，组间拓扑关系满足拓扑排序，但是第 0 组内部不满足拓扑排序。
**代码：**
```python
from collections import defaultdict


class Solution:
    def sortItems(self, n: int, m: int, group: List[int], beforeItems: List[List[int]]) -> List[int]:
        def sort_func(gg, indegree):
            res = []
            while len(indegree) > 0:
                temp = dict(indegree)
                pop_node = [i for i in temp.keys() if temp[i] == 0]
                for i in pop_node:
                    for j in gg[i]:
                        if j in temp:
                            temp[j] -= 1
                    res.append(i)
                    del (temp[i])
                if len(temp) > 0 and temp == indegree:
                    return -1
                indegree = temp
            return res

        aggregate = defaultdict(list)
        cur = -1
        group_map = {}

        for i in range(n):
            if group[i] == -1:
                aggregate[cur].append(i)
                group_map[i] = cur
                cur -= 1
            else:
                aggregate[group[i]].append(i)
                group_map[i] = group[i]

        gg = defaultdict(list)
        gf = defaultdict(list)

        for i in range(n):
            if len(beforeItems[i]) > 0:
                for j in beforeItems[i]:
                    if group_map[j] != group_map[i]:
                        gg[group_map[j]].append(group_map[i])
                        gf[group_map[i]].append(group_map[j])
        indegree = {k: len(gf[k]) for k in aggregate.keys()}
        res = sort_func(gg, indegree)
        if res == -1:
            return []

        final_res = []
        for ii in res:
            innernode = aggregate[ii]
            gg = defaultdict(list)
            gf = defaultdict(list)

            for i in innernode:
                if len(beforeItems[i]) > 0:
                    for j in beforeItems[i]:
                        if group_map[j] == group_map[i]:
                            gg[j].append(i)
                            gf[i].append(j)

            indegree = {k: len(gf[k]) for k in innernode}
            res = sort_func(gg, indegree)
            if res == -1:
                return []
            else:
                final_res += res
        return final_res
```


