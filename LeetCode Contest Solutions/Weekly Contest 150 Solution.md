## [第 150 场周赛](https://leetcode-cn.com/contest/weekly-contest-150)

本周比赛题目难度适中，用到了数学统计、二叉树层序遍历、广度优先搜索（BFS）、后缀数组等算法。

### [1160. 拼写单词](https://leetcode-cn.com/contest/weekly-contest-150/problems/find-words-that-can-be-formed-by-characters)

**思路：**

直接统计字母表 `chars` 中每个字母出现的次数，然后检查词汇表 `words` 中的每个单词，如果该单词中每个字母出现的次数都小于等于词汇表中对应字母出现的次数，就将该单词长度加入答案中。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1160-1.gif)


**代码：**
```python
class Solution:
    def countCharacters(self, words: List[str], chars: str) -> int:
        ans = 0
        cnt = collections.Counter(chars)
        for w in words:
            c = collections.Counter(w)
            if all([c[i] <= cnt[i] for i in c]):
                ans += len(w)
        return ans
```


### [1161. 最大层内元素和](https://leetcode-cn.com/contest/weekly-contest-150/problems/maximum-level-sum-of-a-binary-tree)

**思路：**

用队列进行层序遍历（宽度优先搜索）。把每层结点值相加求和，并更新答案。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1161-1.gif)


**代码：**
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def maxLevelSum(self, root: TreeNode) -> int:
        ans = 1
        step = 1
        maxval = root.val
        q = [root]
        while q:
            t = []
            v = []
            for n in q:
                if n.left:
                    t.append(n.left)
                    v.append(n.left.val)
                if n.right:
                    t.append(n.right)
                    v.append(n.right.val)
            s = sum(v)
            step += 1
            if s > maxval:
                maxval = s
                ans = step
            q = t
        return ans
```


### [1162. 地图分析](https://leetcode-cn.com/contest/weekly-contest-150/problems/as-far-from-land-as-possible)

**思路：**

本题采用广度优先搜索（BFS）算法解答。先将所有陆地的曼哈顿距离设为 0，再把所有陆地结点加入队列，进行广度优先搜索。每次从队列头部弹出一个结点，然后搜索它四周的未访问结点，将这些结点的曼哈顿距离设为当前结点曼哈顿距离加 1，然后加入队列。直到搜索到最后一个结点。搜索过程中不断更新答案。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1162-1.gif)


**代码：**
```python
class Solution:
    def maxDistance(self, grid: List[List[int]]) -> int:
        # 地图规模
        n, m = len(grid), len(grid[0])
        # 每个点到陆地的曼哈顿距离
        dist = [[float('inf') for _ in range(m)] for _ in range(n)]
        # 该点是否被访问过
        visited = [[False for _ in range(m)] for _ in range(n)]
        # 队列
        q = []
        # 陆地计数
        cnt = 0
        ans = 0
        tot = n * m
        for i in range(n):
            for j in range(m):
                if grid[i][j]:
                    dist[i][j] = 0
                    visited[i][j] = True
                    q.append((i, j))
                    cnt += 1
        # 如果都是陆地或者都是海洋，则返回-1
        if cnt == tot or cnt == 0:
            return -1
        while q:
            x, y = q.pop(0) # 出列
            for i, j in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                # 如果坐标合法并且没被访问过
                if 0 <= i < n and 0 <= j < m and not visited[i][j]:
                    dist[i][j] = min(dist[i][j], dist[x][y] + 1) # 取最小值
                    ans = max(ans, dist[i][j]) # 更新答案
                    visited[i][j] = True
                    q.append((i, j)) # 入列
        return ans
```


### [1163. 按字典序排在最后的子串](https://leetcode-cn.com/contest/weekly-contest-150/problems/last-substring-in-lexicographical-order)

**思路：**

按照题意，要求字典序最大的子串，那么一定是该字符串的一个后缀子串，因为如果是中间的一个字串的话，那么只要向它后面继续添加字母，它的字典序一定会更大。然后问题转化为如何求的字典序最大的后缀子串，通常做法是用后缀数组来做。求后缀数组常用做法是基数排序优化的倍增法，时间复杂度 $O(NlogN)$，编程复杂度较小，还有一种 DC3 法虽然可以做到线性复杂度，但是编程难度较大。

此题也可以转换为最大表示法，不过需要对特殊情况做一些判断。

Python3 可以用暴力法通过测试，时间复杂度是 $O(N^2)$


**代码：**

```python
class Solution:
    def lastSubstring(self, s: str) -> str:
        n = len(s)
        ans = ""
        for i in range(n):
            ans = max(ans, s[i:])
        return ans
```


