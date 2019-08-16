## [第 105 场周赛](https://leetcode-cn.com/contest/weekly-contest-105)

本周比赛有一定难度，考察了双指针、二叉树遍历、动态规划等算法。

### [917. 仅仅反转字母](https://leetcode-cn.com/contest/weekly-contest-105/problems/reverse-only-letters)

**思路：**

双指针从两端往中间遍历，如果是字母就交换指针指向的内容，如果不是字母就跳过。

时间复杂度 $O(N)$

空间复杂度 $O(N)$

**图解：**

![图解](http://qiniu.wenyuetech.cn/917-1.gif)


**代码：**
```python
class Solution:
    def reverseOnlyLetters(self, S):
        """
        :type S: str
        :rtype: str
        """
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        s = list(S)
        head = 0
        tail = len(s) - 1
        while head < tail:
            while head < len(s) and s[head] not in alphabet:
                head += 1
            while tail > 0 and s[tail] not in alphabet:
                tail -= 1
            if head < tail:
                s[head], s[tail] = s[tail], s[head]
                head += 1
                tail -= 1
        return ''.join(s)
```


### [918. 环形子数组的最大和](https://leetcode-cn.com/contest/weekly-contest-105/problems/maximum-sum-circular-subarray)

**思路：**

两个思路：一种是将数组复制一份，拼接在原数组后边，用求连续子数组最大和的方法求解，求解过程中需要用一个队列来控制子数组长度不超过原数组的长度；另一种方法更为巧妙，将结果分为两种可能的情况，一种是不跨边界的情况直接求解，一种是跨边界则将问题转化为求解不跨边界的子数组和最小，再用原数组求和减去这个最小值则为最大值，此种方法需要考虑数组中元素全为负数的情况。

时间复杂度 $O(N)$

空间复杂度 $O(N)$


**代码：**

解法1

```python
class Solution:
    def maxSubarraySumCircular(self, A: List[int]) -> int:
        l = len(A)
        A = A + A
        ans = A[0]
        s = [0] * (2 * l)
        q = [0]
        for i in range(1, 2 * l):
            s[i] = s[i - 1] + A[i - 1]
            while q and q[0] < i - l:
                q.pop(0)
            ans = max(ans, s[i] - s[q[0]])
            while q and s[q[-1]] > s[i]:
                q.pop()
            q.append(i)
        return ans
```

解法2

```python
class Solution:
    def maxSubarraySumCircular(self, A: List[int]) -> int:
        result = 0
        curr_max = 0
        result_max = 0
        
        # 分两种情况
        # 一种为没有跨越边界的情况，一种为跨越边界的情况 没有跨越边界的情况直接求子数组的最大和即可
        for num in A:
            curr_max += num
            if curr_max <= 0:
                curr_max = 0
            if curr_max > result_max:
                result_max = curr_max
                
        # 考虑全部为负数的情况
        if result_max == 0:
            result = max(A)
            return result
        
        # 跨越边界的情况可以对数组求和再减去无环的子数组的最小和，即可得到跨越边界情况下的子数组最大和
        curr_min = 0
        result_min = 0
        for num in A:
            curr_min += num
            if curr_min >= 0:
                curr_min = 0
            if curr_min < result_min:
                result_min = curr_min
        
        result = max(result_max, sum(A)-result_min)
        
        return result
```


### [919. 完全二叉树插入器](https://leetcode-cn.com/contest/weekly-contest-105/problems/complete-binary-tree-inserter)

**思路：**

对完全二叉树每个结点进行编号，空二叉树标记为 `0`，根结点标记为 `1`，根结点的左儿子标记为 `10`，根结点的右儿子标记为 `11`，之后，每个结点如果是左儿子，就在父结点的编号后面增加一个 `0`，如果是右儿子，就在父结点的编号后面增加一个 `1`，以此类推。这样，完全二叉树的每个结点编号其实就代表了它是层次遍历中第几个结点的二进制编码，比如根结点是第一个结点，编号为 `1`，二进制为 `1`，根结点左儿子是第二个结点，编号为 `2`，二进制为 `10`，以此类推，每个结点的编号二进制就可以代表从根结点到这个结点的一个路径，从编号二进制的第二位开始，如果为 `0` 就走左子树，如果为 `1` 就走右子树。所以我们只需要动态维护完全二叉树的总结点个数，就可以知道插入结点在哪个位置了。

时间复杂度 初始化为 $O(N)$ 插入为 $O(logN)$ 返回根结点为 $O(1)$

空间复杂度 $O(N)$

**图解：**

![图解](http://qiniu.wenyuetech.cn/919-1.gif)


**代码：**
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class CBTInserter:

    def __init__(self, root: TreeNode):
        self.r = root
        
        def dfs(root):
            if not root:
                return 0
            return dfs(root.left) + dfs(root.right) + 1
        
        self.n = dfs(root)

    def insert(self, v: int) -> int:
        self.n += 1
        x = self.n
        path = []
        while x > 0:
            path.insert(0, x % 2)
            x //= 2
        father = self.r
        for i in range(1, len(path) - 1):
            if path[i] == 0:
                father = father.left
            else:
                father = father.right
        t = TreeNode(v)
        if path[-1] == 0:
            father.left = t
        else:
            father.right = t
        return father.val

    def get_root(self) -> TreeNode:
        return self.r


# Your CBTInserter object will be instantiated and called as such:
# obj = CBTInserter(root)
# param_1 = obj.insert(v)
# param_2 = obj.get_root()
```
### [920. 播放列表的数量](https://leetcode-cn.com/contest/weekly-contest-105/problems/number-of-music-playlists)

**思路：**

动态规划：我们用 `dp[i][j]` 代表 `i` 首不同的歌，要听 `j` 首歌组成的播放列表，有多少种情况，那么 `dp[N][L]` 即是我们所要求得的结果。显然，当 `i == j` 时，可能的方案为 `i` 的全排列。由于每一首歌都要在其他 `K` 首歌播放完后才能再次播放，所以当 `i == K + 1` 时，歌曲只能按照一种排列循环，所以方案数也是 `i` 的阶乘。我们已知当前列表已经有 `j - 1` 首歌的方案数，需要求有 `j` 首歌的方案数时，有两种情况，一种是播放一首从来没有播放过的歌，可以有 `i` 种选法，即 `dp[i - 1][j - 1] * i`，另一种是播放一首已经播放过的歌，但是这首歌不能在最后 `K` 首歌之中，即 `dp[i][j - 1] * (i - K)`。于是可求得状态转移方程为 `dp[i][j] = dp[i - 1][j - 1] * i + dp[i][j - 1] * (i - K)`。

时间复杂度 $O(NL)$

空间复杂度 $O(NL)$


**代码：**
```python
class Solution:
    def numMusicPlaylists(self, N: int, L: int, K: int) -> int:
        dp = [[0] * (L + 1) for _ in range(N + 1)]
        for i in range(K + 1, N + 1):
            for j in range(i, L + 1):
                if i == j or i == K + 1:
                    dp[i][j] = math.factorial(i)
                else:
                    dp[i][j] = dp[i - 1][j - 1] * i + dp[i][j - 1] * (i - K)
        return dp[N][L] % (10 ** 9 + 7)
```


