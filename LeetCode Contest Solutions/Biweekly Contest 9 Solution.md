## [第 9 场双周赛](https://leetcode-cn.com/contest/biweekly-contest-9)

本周比赛考察了排序、广度优先搜索、数学、统计、贪心等算法。

### [1196. 最多可以买到的苹果数量](https://leetcode-cn.com/contest/biweekly-contest-9/problems/how-many-apples-can-you-put-into-the-basket)

**思路：**

贪心算法，先排序，然后从最小的苹果开始取，一直取到购物袋装不下苹果为止。


**代码：**
```python
class Solution:
    def maxNumberOfApples(self, arr: List[int]) -> int:
        arr.sort()
        cap = 0
        ans = 0
        while ans < len(arr):
            if cap + arr[ans] <= 5000:
                cap += arr[ans]
                ans += 1
            else:
                break
        return ans
```


### [1197. 进击的骑士](https://leetcode-cn.com/contest/biweekly-contest-9/problems/minimum-knight-moves)

**思路：**

广度优先搜索：

1. 如果 `(x, y) == (0, 0)`，那么直接返回 `0`，否则将 `(0, 0)` 加入队列和集合 `visited`，并置 `ans = 1`；
2. 每次从队列中弹出结点，并以该结点坐标为基础，向八个方向查找，是否有坐标满足答案；
3. 如果满足答案，直接返回 `ans`；
4. 如果不满足答案，并且坐标不在 `visited` 中，则将结点加入新队列和 `visited`；
5. 当前队列遍历完毕，将指针指向新队列，并且 `ans += 1`，重复步骤2，直到找到答案。

朴素的 BFS 会超时，这里我们需要注意，棋盘是关于 x 轴和 y 轴对称的，那么我们只需要将目标坐标取绝对值，在第一象限查找即可。

还有一种数学方法，棋盘还关于 $ y = \pm x$ 对称，我们将 x 和 y 处理为第一象限的右下方部分，使 $ 0 \leq y \le x $ ，我们可以使用下列公式求得结果：

$$f(x, y)=
\begin{cases}
\delta - 2 \left \lfloor \frac{\delta - y}{3} \right \rfloor & y < \delta \\
\delta - 2 \left \lfloor \frac{\delta - y}{4} \right \rfloor & \text{otherwise}
\end{cases} \text{where } \delta = x - y$$
但是，需要判断两个 corner case：`f(1, 0) = 3` 和 `f(2, 2) = 4`。


**代码：**

BFS

```python
class Solution:
    def minKnightMoves(self, x: int, y: int) -> int:
        if x == 0 and y == 0:
            return 0
        x, y = abs(x), abs(y)
        dd = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
        visited = set([(0, 0)])
        q = [(0, 0)]
        ans = 0
        while q:
            ans += 1
            t = []
            while q:
                xx, yy = q.pop()
                for dx, dy in dd:
                    i = xx + dx
                    j = yy + dy
                    if i < 0 or j < 0 or abs(i) + abs(j) > 400:
                        continue
                    if i == x and j == y:
                        return ans
                    elif (i, j) not in visited:
                        visited.add((i, j))
                        t.append((i, j))
            q = t             
```

数学方法

```python
class Solution:
    def minKnightMoves(self, x: int, y: int) -> int:
        # axes symmetry 
        x, y = abs(x), abs(y)
        # diagonal symmetry 
        if x < y: x, y = y, x
        # 2 corner cases
        if (x, y) == (1, 0): return 3
        if (x, y) == (2, 2): return 4
        # main formula
        delta = x - y
        if y > delta:
            return delta - 2 * ((delta - y) // 3)
        else:
            return delta - 2 * ((delta - y) // 4)
```


### [1198. 找出所有行中最小公共元素](https://leetcode-cn.com/contest/biweekly-contest-9/problems/find-smallest-common-element-in-all-rows)

**思路：**

统计所有数字出现的个数，每行相同的数字只统计一次，那么公共的元素个数肯定等于行数 n。最后从小到大遍历统计过的数字，第一个出现次数为 n 的数就是答案。


**代码：**
```python
class Solution:
    def smallestCommonElement(self, mat: List[List[int]]) -> int:
        cnt = [0] * 10001
        n, m = len(mat), len(mat[0])
        for i in range(n):
            cnt[mat[i][0]] += 1
            for j in range(1, m):
                if mat[i][j] != mat[i][j - 1]:
                    cnt[mat[i][j]] += 1
        for ans in range(1, 10001):
            if cnt[ans] == n:
                return ans
        return -1
```


### [1199. 建造街区的最短时间](https://leetcode-cn.com/contest/biweekly-contest-9/problems/minimum-time-to-build-blocks)

**思路：**

这道题目类似于构建哈夫曼树，可以采用贪心的方法解决。根据题意，初始情况只有一个工人，而且一个工人只能建造一个街区，那么如果我们要建造 n 个街区，必然要将工人分裂 n - 1 次。不同方案的区别就在于，每一步分裂的工人是有两个选择，一个选择是直接去建造街区，另一个选择是开始下一步的分裂。所以我们可以将分裂过程看成一棵二叉树，初始的工人在根节点，每分裂一次，就生成两个儿子，消耗 `split` 个单位时间，如果不分裂，就变成叶子节点建造街区。显然，随着树深度的增加，分裂花费的时间也在增加，深度为 `depth` 的节点，所需分裂时间是 `depth * split`。所以，要想总花费时间最小，就要给深度大的节点分配建造时间少的街区，给深度小的节点分配建造时间多的街区，最终答案就是每个节点的 `block[i] + depth * split` 取最大值。

树的构造过程和哈夫曼树构造过程相似，用优先队列，每次取时间花费最少的两个节点，增加他们的分裂层数，合并为一个新节点，该节点的权值取两者权值较大的那个，再加上 `split`。如此操作 n - 1 次，得到最后的节点值就是答案。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1199-1.gif)


**代码：**
```python
import heapq

class Solution:
    def minBuildTime(self, blocks: List[int], split: int) -> int:
        n = len(blocks)
        if n == 1: return blocks[0]
        heapq.heapify(blocks)
        for i in range(n - 1):
            a = heapq.heappop(blocks)
            b = heapq.heappop(blocks)
            c = b + split
            heapq.heappush(blocks, c)
        return blocks[0]
```


