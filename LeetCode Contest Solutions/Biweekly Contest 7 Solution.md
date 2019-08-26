## [第 7 场双周赛](https://leetcode-cn.com/contest/biweekly-contest-7)

本周比赛比较考查一些思维能力，用到了数学运算、字符串处理、优先队列、最小生成树等算法。

### [1165. 单行键盘](https://leetcode-cn.com/contest/biweekly-contest-7/problems/single-row-keyboard)

**思路：**

用字典将每个字母和它的位置进行映射，然后遍历 `word`，根据字母的位置计算每次移动的距离，进行加和得到答案。


**代码：**
```python
class Solution:
    def calculateTime(self, keyboard: str, word: str) -> int:
        d = dict()
        for i in range(26):
            d[keyboard[i]] = i
        p, ans = 0, 0
        for c in word:
            ans += abs(d[c] - p)
            p = d[c]
        return ans
```


### [1166. 设计文件系统](https://leetcode-cn.com/contest/biweekly-contest-7/problems/design-file-system)

**思路：**

建一个字典，存储路径到值的映射。在 `create` 操作时，检查路径的父路径，如果不存在，则返回 `False`，存在则将路径和值加入字典，并返回 `True`。`get` 操作直接从字典中返回值即可，不存在返回 `-1`。


**代码：**
```python
class FileSystem:

    def __init__(self):
        self.d = dict()

    def create(self, path: str, value: int) -> bool:
        if path == "/":
            return False
        p = path.split('/')
        n = len(p)
        if n > 2 and '/'.join(p[:n-1]) not in self.d:
            return False
        self.d[path] = value
        return True
        

    def get(self, path: str) -> int:
        if path not in self.d:
            return -1
        return self.d[path]


# Your FileSystem object will be instantiated and called as such:
# obj = FileSystem()
# param_1 = obj.create(path,value)
# param_2 = obj.get(path)
```


### [1167. 连接棒材的最低费用](https://leetcode-cn.com/contest/biweekly-contest-7/problems/minimum-cost-to-connect-sticks)

**思路：**

根据题意，`n` 根棒材，需要进行 `n-1` 次操作才能连接成一根棒材。如果要将长度分别为 `X` 和 `Y` 的两根棒材连接在一起，你需要支付 `X + Y` 的费用，所以，我们需要让短的棒材在操作中出现的次数尽量多，这是一个带权最短路径的二叉树问题，用构造哈夫曼树来解决。

给定 `N` 个权值作为 `N` 个叶子结点，构造一棵二叉树，若该树的带权路径长度达到最小，称这样的二叉树为最优二叉树，也称为哈夫曼树（Huffman Tree）。哈夫曼树是带权路径长度最短的树，权值较大的结点离根较近。

构造哈夫曼树可以将所有结点加入一个最小堆，每次从最小堆中弹出两最小的结点，将他们组合，重新加入最小堆，如此往复直到最小堆中只剩下一个结点。过程中所有操作花费的和即为答案。


**代码：**
```python
import heapq

class Solution:
    def connectSticks(self, sticks: List[int]) -> int:
        heapq.heapify(sticks)
        ans = 0
        n = len(sticks)
        for i in range(1, n):
            a = heapq.heappop(sticks)
            b = heapq.heappop(sticks)
            c = a + b
            ans += c
            heapq.heappush(sticks, c)
        return ans
```


### [1168. 水资源分配优化](https://leetcode-cn.com/contest/biweekly-contest-7/problems/optimize-water-distribution-in-a-village)

**思路：**

把水源看成第 `0` 个结点，把 `wells[i]` 看成结点 `0` 到结点 `i + 1` 边的权值，那么结果就是求一个最小生成树的花费。由于 `1 <= n <= 10000` 且 `1 <= pipes.length <= 10000`，可以看出这是一个稀疏图，所以用并查集优化的克鲁斯卡尔（kruskal）算法比较方便。算法具体过程可以参看 [第 5 场双周赛](https://leetcode-cn.com/contest/biweekly-contest-5) 题目 [1135. 最低成本联通所有城市](https://leetcode-cn.com/problems/connecting-cities-with-minimum-cost) 的解答。


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
    def minCostToSupplyWater(self, n: int, wells: List[int], pipes: List[List[int]]) -> int:
        connections = []
        for i, w in enumerate(wells):
            connections.append((w, 0, i + 1))
        for i, j, w in pipes:
            connections.append((w, i, j))
        connections.sort()
        ans, cnt = 0, 0
        dsu = DSU(n + 1)
        for w, x, y in connections:
            if dsu.find(x) != dsu.find(y):
                ans += w
                cnt += 1
                if cnt == n:
                    return ans
                dsu.union(x, y)
        return ans
```


