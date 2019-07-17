## [第 145 场周赛](https://leetcode-cn.com/contest/weekly-contest-145)

本周比赛题目比较难，考察对题目的理解和编程技巧，其中第三题多种解法，想要在比赛中写出最优解法比较困难。本周比赛用到的算法有排序、深度优先搜索、二分、数组前缀和、单调栈、动态规划等等。

### [1122. 数组的相对排序](https://leetcode-cn.com/contest/weekly-contest-145/problems/relative-sort-array)

**思路：**

先把数组`arr1`分成两部分，一部分是存在于`arr2`中的数，另一部分是不存在于`arr2`中的数。对于第二部分，很容易，我们可以直接排序，放在第一部分的后面。对于第一部分的数，要按照`arr2`中的数字顺序排序，那么我们其实可以统计`arr2`中的数在这部分出现了多少次，然后遍历`arr2`的同时，在答案数组中加入相同频次的这个数字即可。


**代码：**
```python
class Solution:
    def relativeSortArray(self, arr1: List[int], arr2: List[int]) -> List[int]:
        not_exist = []
        exist = []
        s = set(arr2)
        ans = []
        for a in arr1:
            if a in s:
                exist.append(a)
            else:
                not_exist.append(a)
        cnt = collections.Counter(exist)
        for a in arr2:
            ans += [a] * cnt[a]
        return ans + sorted(not_exist)
```
### [1123. 最深叶节点的最近公共祖先](https://leetcode-cn.com/contest/weekly-contest-145/problems/lowest-common-ancestor-of-deepest-leaves)

**思路：**

题目要返回最深叶结点的最近公共祖先。由于最深的叶结点可能有多个（如果只有一个最深的叶结点，那么它的最近公共祖先就是它自己），我们观察它们最近公共祖先的性质。首先，我们可以看出最近公共祖先的两个子树是等高的，如果不等高，那么高度较小的那个子树叶结点必然不是最深。所以我们可以设计这样的深度优先搜索算法，每一层返回值有两部分组成：一部分是以该结点为根的子树中，最深叶结点的公共祖先，另一部分是该层的高度（也即该结点到其最深叶结点的深度）。然后我们可以递归比较：

1. 如果一个结点的左子树和右子树高度相等，那么其左子树的最深结点和右子树的最深结点，都是以这个结点为根的最深叶结点，那么我们就返回这个结点，和这个结点的高度（左子树高度或右子树高度加1）；
2. 如果一个结点的左子树高度大于右子树，那么以这个结点为根的树，其最深叶结点一定在左子树中，那么我们就返回其左子树中最深结点的最近公共祖先，和当前结点的高度（左子树高度加1）；
3. 如果一个结点的右子树高度大于左子树，那么我们处理情况和情况2相反，返回右子树中最深结点的最近公共祖先，和当前结点的高度（右子树高度加1）。


**代码：**
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def lcaDeepestLeaves(self, root: TreeNode) -> TreeNode:
        def dfs(root):
            if not root:
                return None, 0
            lr, ld = dfs(root.left)
            rr, rd = dfs(root.right)
            if ld > rd:
                return lr, ld + 1
            elif ld < rd:
                return rr, rd + 1
            else:
                return root, ld + 1
        ans, h = dfs(root)
        return ans
```
### [1124. 最长的表现良好时间段](https://leetcode-cn.com/contest/weekly-contest-145/problems/longest-well-performing-interval)

**思路：**

本题有多种方法，暴力的方法时间复杂度是$O(N^2)$，用二分法可以将时间复杂度降为$O(NlogN)$ ，下面介绍用单调栈可以实现$O(N)$时间复杂度的方法。其实本题变形后与[962. 最大宽度坡](https://leetcode-cn.com/problems/maximum-width-ramp/)类似。

以输入样例`hours = [9,9,6,0,6,6,9]`为例，我们将大于8小时的一天记为1分，小于等于8小时的一天记为-1分。那么处理后，我们得到`score = [1, 1, -1, -1, -1, -1, 1]`，然后我们对得分数组计算前缀和`presum = [0, 1, 2, 1, 0, -1, -2, -1]`。题目要求返回表现良好时间段的最大长度，即求最长的一段中，得分1的个数大于得分-1的个数，也就是求`score`数组中最长的一段子数组，其和大于0，那么也就是找吹前缀和数组`presum`中两个索引`i`和`j`，使`j - i`最大，且保证`presum[j] - presum[i]`大于0。到此，我们就将这道题转化为，求`presum`数组中的一个最长的上坡，可以用单调栈实现。我们维护一个单调栈，其中存储`presum`中的元素索引，栈中索引指向的元素严格单调递减，由`presum`数组求得单调栈为`stack = [0, 5, 6]`， 其表示元素为`[0, -1, -2]`。然后我们从后往前遍历`presum`数组，与栈顶索引指向元素比较，如果相减结果大于0，则一直出栈，直到不大于0为止，然后更新当前最大宽度。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1124-1.gif)

**代码：**
```python
class Solution:
    def longestWPI(self, hours: List[int]) -> int:
        n = len(hours)
        # 大于8小时计1分 小于等于8小时计-1分
        score = [0] * n
        for i in range(n):
            if hours[i] > 8:
                score[i] = 1
            else:
                score[i] = -1
        # 前缀和
        presum = [0] * (n + 1)
        for i in range(1, n + 1):
            presum[i] = presum[i - 1] + score[i - 1]
        ans = 0
        stack = []
        # 顺序生成单调栈，栈中元素从第一个元素开始严格单调递减，最后一个元素肯定是数组中的最小元素所在位置
        for i in range(n + 1):
            if not stack or presum[stack[-1]] > presum[i]:
                stack.append(i)
        # 倒序扫描数组，求最大长度坡
        i = n
        while i > ans:
            while stack and presum[stack[-1]] < presum[i]:
                ans = max(ans, i - stack[-1])
                stack.pop()
            i -= 1
        return ans
```
### [1125. 最小的必要团队](https://leetcode-cn.com/contest/weekly-contest-145/problems/smallest-sufficient-team)

**思路：**

本题是一个[集合覆盖问题](https://baike.baidu.com/item/%E9%9B%86%E5%90%88%E8%A6%86%E7%9B%96%E9%97%AE%E9%A2%98/9160069)，[决定性问题](https://baike.baidu.com/item/决定性问题)的集合覆盖是[NP完全问题](https://baike.baidu.com/item/NP完全问题)，最佳化问题的集合覆盖是NP困难问题。所以想得到最优解（之一），只能用暴力搜索。好在数据范围并不大，最大状态空间也只有$2^{16}=65,536‬$种状态，也就是16个人每个人有选和不选两种情况。我们可以用动态规划的方法进行搜索。先将`req_skills`的全集建立一个字典，对每个技能进行编号`0 ~ n-1`。然后建立`dp`数组，长度为$2^n$，数组元素初始化为`people`的全集，然后对`dp[0]`初始化为空集。然后我们遍历每个人，对于所有状态，计算把这个人加入团队后，整个团队的技能是否增加，如果增加并且人数比拥有相同技能的团队更优化，则更新结果。最终，全集`dp[(1 << n) - 1]`中的`people`集合就是我们要求的结果。


**代码：**
```python
class Solution:
    def smallestSufficientTeam(self, req_skills: List[str], people: List[List[str]]) -> List[int]:
        # 为skills建立字典
        n = len(req_skills)
        d = dict()
        for i in range(n):
            d[req_skills[i]] = i
        # 所有状态
        dp = [list(range(len(people))) for _ in range(1 << n)]
        dp[0] = []
        # 遍历所有人
        for i in range(len(people)):
            # 求这个人的技能
            skill = 0
            for s in people[i]:
                skill |= (1 << d[s])
            for k, v in enumerate(dp):
                # 把这个人加入进来以后的团队技能
                new_skills = k | skill
                # 如果团队技能因此而增加 并且增加后的人数比新技能原来的人数少 则更新答案
                if new_skills != k and len(dp[new_skills]) > len(v) + 1:
                    dp[new_skills] = v + [i]
        return dp[(1 << n) - 1]
```


