## [第 148 场周赛](https://leetcode-cn.com/contest/weekly-contest-148)

本周比赛题目算法方面不是很难，主要在于理解题意和编程实现，考察的算法有数学上的分类讨论、二叉树的深度优先搜索、二分查找、贪心等。

### [1144. 递减元素使数组呈锯齿状](https://leetcode-cn.com/contest/weekly-contest-148/problems/decrease-elements-to-make-array-zigzag)

**思路：**

根据题意，我们遍历数组，分两种情况讨论，要么将奇数位置的元素减少到刚好比相邻的偶数位置元素小，要么将偶数位置的元素减少到刚好比相邻的奇数位置元素小。返回两种情况操作较少的作为答案。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1144-1.png)

以输入样例 `[9, 6, 1, 6, 2]` 为例，检查奇数位置，可以将第一个元素 `9` 减小到 `5`，如果检查偶数位置，则需要将两个 `6` 减小到 `0`。


**代码：**
```python
class Solution:
    def movesToMakeZigzag(self, nums: List[int]) -> int:
        n = len(nums)
        ans1, ans2 = 0, 0
        for i in range(n):
            # 奇数位置
            if i % 2 == 0:
                d1 = nums[i] - nums[i - 1] + 1 if i > 0 and nums[i] >= nums[i - 1] else 0
                d2 = nums[i] - nums[i + 1] + 1 if i < n - 1 and nums[i] >= nums[i + 1] else 0
                ans1 += max(d1, d2)
            # 偶数位置
            else:
                d1 = nums[i] - nums[i - 1] + 1 if nums[i] >= nums[i - 1] else 0
                d2 = nums[i] - nums[i + 1] + 1 if i < n - 1 and nums[i] >= nums[i + 1] else 0
                ans2 += max(d1, d2)
        return min(ans1, ans2)
```


### [1145. 二叉树着色游戏](https://leetcode-cn.com/contest/weekly-contest-148/problems/binary-tree-coloring-game)

**思路：**

![示意图](http://qiniu.wenyuetech.cn/1145-1.png)

如图所示，当一号玩家选择了一个红色的结点，可能会将二叉树切割为 3 个部分（连通分量），如果选择的是根结点，则可能是 2 个部分或 1 个部分，如果选择叶结点，则是 1 个部分。不过无论哪种情况都无关紧要，我们都可以当成 3 个部分来对待，例如一号玩家选择了一个叶结点，我们也可以把叶结点的左右两个空指针看成大小为 0 的两个部分。

下面我们就来思考，**二号玩家怎样选择蓝色结点才是最优呢**？答案是：选择离红色结点最近，且所属连通分量规模最大的那个点。也就是示例图中的 1 号结点。如果我们选择了 1 号结点为蓝色结点，那么可以染成红色的点就只剩下 6 号点和 7 号点了，而蓝色可以把根结点和其左子树全部占据。

如何确定蓝色是否有必胜策略，就可以转换为，被红色点切割的三个连通分量中，**是否存在一个连通分量，大小大于所有结点数目的一半**。统计三个连通分量大小的过程，可以用深度优先搜索（DFS）来实现。当遍历到某一结点，其结点值等于选定的红色结点时，我们统计这个结点的左子树 `red_left` 和右子树 `red_right` 的大小，那么我们就已经找到两个连通分量的大小了，最后一个父结点连通分量的大小，可以用结点总数减去这两个连通分量大小，再减去红色所占结点，即 `parent = n - red_left - red_right - 1`。


**代码：**
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def btreeGameWinningMove(self, root: TreeNode, n: int, x: int) -> bool:
        self.red_left, self.red_right = 0, 0
        
        def dfs(root):
            if not root:
                return 0
            left = dfs(root.left)
            right = dfs(root.right)
            if root.val == x:
                self.red_left = left
                self.red_right = right
            return left + right + 1
        
        dfs(root)
        parent = n - self.red_left - self.red_right - 1
        judge = [parent, self.red_left, self.red_right]
        return any([j > n // 2 for j in judge])
```


### [1146. 快照数组](https://leetcode-cn.com/contest/weekly-contest-148/problems/snapshot-array)

**思路：**

由于快照功能 `snap()` 的调用次数可能很多，所以我们如果采用每次快照都整体保存一次数组的方法，无论在时间复杂度还是空间复杂度上，都是行不通的。那么更优化的方法是，只保存每次快照变化的部分。所以我们建立的不是一个数组，而是要建立一个哈希字典数组，每个字典的索引是快照的 `snap_id`，这样，我们在返回某个快照的元素值时，只需要查找这个快照 `snap_id` 前的最后一次修改即可。

查找的方式可以采用二分搜索的方式来降低时间复杂度。


**代码：**
```python
class SnapshotArray:

    def __init__(self, length: int):
        # 初始化字典数组和 id
        self.arr = [{0: 0} for _ in range(length)]
        self.sid = 0

    def set(self, index: int, val: int) -> None:
        # 设置当前快照的元素值
        self.arr[index][self.sid] = val

    def snap(self) -> int:
        # 每次快照 id 加 1
        self.sid += 1
        # 返回上一个快照 id
        return self.sid - 1

    def get(self, index: int, snap_id: int) -> int:
        # 选择要查找的元素的字典
        d = self.arr[index]
        # 如果快照恰好存在, 直接返回
        if snap_id in d:
            return d[snap_id]
        # 不存在则进行二分搜索, 查找快照前最后一次修改
        k = list(d.keys())
        i = bisect.bisect_left(k, snap_id)
        return d[k[i - 1]]


# Your SnapshotArray object will be instantiated and called as such:
# obj = SnapshotArray(length)
# obj.set(index,val)
# param_2 = obj.snap()
# param_3 = obj.get(index,snap_id)
```


### [1147. 段式回文](https://leetcode-cn.com/contest/weekly-contest-148/problems/longest-chunked-palindrome-decomposition)

**思路：**

双指针从两端往中间遍历，用两个字符串不断加入指针所指向的字符，更新并比较，相等则答案加 2，并清空字符串继续遍历。如果最后遍历完，有剩余字符串，那么答案再加 1。

![贪心正确性](http://qiniu.wenyuetech.cn/1147-2.png)

下面我们来简单说明一下贪心的正确性。如上图，当我们从两边向中间遍历，首先得到两个相等的字符串 `a` 的时候，如果我们不进行局部贪心，而继续扫描，那么我们找到的下一组段式回文对，前者必然要包含后缀 `a`，后者必然要包含前缀 `a`，而且中间的 `b` 字符串必然也要相等，那么这组段式回文对就一定可以拆出大于等于 3 对的段式回文对。所以局部贪心是最优的。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1147-1.gif)


**代码：**
```python
class Solution:
    def longestDecomposition(self, text: str) -> int:
        n = len(text)
        i, j = 0, n - 1
        str1, str2, ans = '', '', 0
        while i < j:
            str1 = str1 + text[i]
            str2 = text[j] + str2
            if str1 == str2:
                ans += 2
                str1, str2 = '', ''
            i += 1
            j -= 1
        if n % 2 == 1 or str1 != '':
            ans += 1
        return ans
```


