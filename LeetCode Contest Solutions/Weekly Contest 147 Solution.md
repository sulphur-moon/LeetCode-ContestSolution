## [第 147 场周赛](https://leetcode-cn.com/contest/weekly-contest-147)

本周比赛题目比较难，解题需要一些技巧，考察的算法有递推、坐标运算、前缀和、动态规划等。

### [1137. 第 N 个泰波那契数](https://leetcode-cn.com/contest/weekly-contest-147/problems/n-th-tribonacci-number)

**思路：**

直接根据题干公式 `T[n + 3] = T[n] + T[n + 1] + T[n + 2]` 进行递推即可。


**代码：**
```python
class Solution:
    def tribonacci(self, n: int) -> int:
        ans = [0, 1, 1]
        if n < 3:
            return ans[n]
        for i in range(3, n + 1):
            ans.append(ans[i - 3] + ans[i - 2] + ans[i - 1])
        return ans[n]
```


### [1138. 字母板上的路径](https://leetcode-cn.com/contest/weekly-contest-147/problems/alphabet-board-path)

**思路：**

乍一看，此题像是一道搜索题，但是仔细观察，alphabet board 上面的每个字母都是有固定横纵坐标的，所以我们直接遍历 target，再根据相对坐标运算得出答案。但是在生成答案的时候需要注意一个特殊情况，就是最后一行只有一个字母 `z`，当前字符为 `z` 的时候，不能从字母 `z` 的右边到达，只能从上边到达。而上一个字符为字母 `z` 的时候，我们不能从字母 `z` 的右边出发，只能从字母 `z` 的上边出发。所以我们需要优化一个答案生成顺序，优先生成左 `L` 上 `U`，即可避免移动出 alphabet board 的非法路径。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1138-1.gif)


**代码：**
```python
class Solution:
    def alphabetBoardPath(self, target: str) -> str:
        x, y, d = 0, 0, dict()
        for i in range(26):
            d[chr(i + 97)] = (i // 5, i % 5)
        cur, ans = (0, 0), []
        for c in target:
            nxt = d[c]
            dx, dy = nxt[0] - cur[0], nxt[1] - cur[1]
            if dx < 0: ans += ['U'] * (-dx)
            if dy < 0: ans += ['L'] * (-dy)
            if dx > 0: ans += ['D'] * dx
            if dy > 0: ans += ['R'] * dy
            ans.append('!')
            cur = nxt
        return ''.join(ans)
```


### [1139. 最大的以 1 为边界的正方形](https://leetcode-cn.com/contest/weekly-contest-147/problems/largest-1-bordered-square)

**思路：**

从大到小枚举可能的边长，最大的边长为 `min(grid, grid[0])`，然后枚举起始坐标，检查以起始坐标为左上端点的、并且以 1 为界的正方形是否存在。如果我们直接检查正方形的边界是否都为 1，那么总的时间复杂度会达到 $O(N^4)$，所以我们需要在检查边长的时候做一些优化，避免重复检查矩阵元素是否为 1。用前缀和的方法可以达到这个效果。我们用 `L[i][j]` 表示 `(i, j)` 的左边有多少个 1，用 `U[i][j]` 表示 `(i, j)` 的上边有多少个 1，那么我们就可以计算一条边两个端点的差值，看看这个差值是否和边的长度相等就可以了。优化后的时间复杂度降为 $O(N^3)$。

**图解：**

![边界符合条件的检查过程](http://qiniu.wenyuetech.cn/1139-1.gif)


**代码：**
```python
class Solution:
    def largest1BorderedSquare(self, grid: List[List[int]]) -> int:
        # 矩阵规模
        n, m, s = len(grid), len(grid[0]), 0
        # 四个方向上的前缀和
        L, U = [[[0] * (m + 1) for i in range(n + 1)] for j in range(2)]
        for i in range(n):
            for j in range(m):
                # 矩阵和
                s += grid[i][j]
                # L[i][j] 表示 (i, j) 的左边有多少个 1
                L[i][j + 1] = L[i][j] + grid[i][j]
                # U[i][j] 表示 (i, j) 的上边有多少个 1
                U[i + 1][j] = U[i][j] + grid[i][j]
        if s == 0:
            return 0
        # 四条边上 1 的个数
        edges = [0, 0, 0, 0]
        for e in range(min(n, m), 0, -1):
            for i in range(n - e + 1):
                for j in range(m - e + 1):
                    # 判断上边
                    edges[0] = L[i][j + e] - L[i][j]
                    # 判断下边
                    edges[1] = L[i + e - 1][j + e] - L[i + e - 1][j]
                    # 判断左边
                    edges[2] = U[i + e][j] - U[i][j]
                    # 判断右边
                    edges[3] = U[i + e][j + e - 1] - U[i][j + e - 1]
                    # 判断是否满足
                    if all([edge == e for edge in edges]):
                        return e * e
        return 0
```


### [1140. 石子游戏 II](https://leetcode-cn.com/contest/weekly-contest-147/problems/stone-game-ii)

**思路：**

本题难点在于理解两者都发挥“最佳水平”，“最佳水平”在于，每当轮到自己拿石子的时候，要在后继的所有状态中，选择对自己最有利的，那么也就是要遍历后继的所有状态，并选择一个最优解。我们设 `dfs(i, M)` 表示，当从第 `i` 堆石子开始拿，允许拿 `M <= x <= 2 * M` 时，在剩余石子中所能拿到的最大值，那么我们最终要返回的结果就是 `dfs(0, 1)`。搜索状态时，我们要遵循以下几个原则：

1. 如果 `i >= n`，那么说明石子都已经拿完，直接返回 `0`；
2. 如果 `i + M * 2 >= n`，那么说明可以把剩余石子一起拿到，就可以直接返回剩余石子的数目 `sum(piles[i:])`；
3. 如果不属于以上两种情况，那么我们需要遍历 `1 <= x <= 2 * M`，求剩余的最小 `dfs(i + x, max(x, M))`，也就是自己拿多少的时候，对手拿的石子最少（由于剩余石子数固定，那么最小化对手石子数，就是最大化自己的石子数）。

为了防止重复搜索，可以采用记忆化的方法。为了快速求剩余石子数目，可以提前处理后缀和。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1140-1.png)

如图所示， `dfs(i, M)` 表示，当从第 `i` 堆石子开始拿，允许拿 `M <= x <= 2 * M` 时，在剩余石子中所能拿到的最大值。蓝色块代表先手拿的状态，黄色块代表后手拿的状态。边上的权值代表拿了几堆石子（也就是 `x`），红色边代表当前层最优解，连续的红色路径就是答案。


**代码：**
```python
class Solution:
    def stoneGameII(self, piles: List[int]) -> int:
        # 数据规模与记忆化
        n, memo = len(piles), dict()
        
        # s[i] 表示第 i 堆石子到最后一堆石子的总石子数
        s = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            s[i] = s[i + 1] + piles[i]
            
        # dfs(i, M) 表示从第 i 堆石子开始取，最多能取 M 堆石子所能得到的最优值
        def dfs(i, M):
            # 如果已经搜索过，直接返回
            if (i, M) in memo:
                return memo[(i, M)]
            # 溢出拿不到任何石子
            if i >= n:
                return 0
            # 如果剩余堆数小于等于 2M， 那么可以全拿走
            if i + M * 2 >= n:
                return s[i]
            # 枚举拿 x 堆的最优值
            best = 0
            for x in range(1, M * 2 + 1):
                # 剩余石子减去对方最优策略
                best = max(best, s[i] - dfs(i + x, max(x, M)))
            # 记忆化
            memo[(i, M)] = best
            return best
        
        return dfs(0, 1)
```


