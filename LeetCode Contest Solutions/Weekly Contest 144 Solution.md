## Weekly Contest 144 Solution

本周比赛题目除了第一道题很简单以外，后三道题都需要一些编程技巧，考察了数组前缀和、扫描线，二叉树的深度优先搜索，字符串处理，栈的深度等知识。

### [1108.IP 地址无效化](https://leetcode-cn.com/contest/weekly-contest-144/problems/defanging-an-ip-address/)

**思路：**

这是一道简单题，直接用字符串处理函数将`"."`替换为`"[.]"`即可。


**代码：**
```python
class Solution:
    def defangIPaddr(self, address: str) -> str:
        return address.replace(".", "[.]")
```


### [1109.航班预订统计](https://leetcode-cn.com/contest/weekly-contest-144/problems/corporate-flight-bookings/)


**思路：**

本题数据范围是`20000`，直接加的暴力方法会超时，需要优化到线性时间才行，考虑前缀和或者线性扫描，本质是一样的。题目中`bookings`每一项给出了一个区间，包含区间的开始位置、结束位置和区间值，当我们从左到右遍历答案数组时，进入这个区间就要加上这个区间的值，出这个区间就要减去这个区间的值，所以我们只需要用字典或者在数组中记录一下区间端点和相应的值，再从左到右扫描一遍数组即可。

**图解：**

![前缀和法](http://qiniu.wenyuetech.cn/1109-1.gif)

![线性扫描法](http://qiniu.wenyuetech.cn/1109-2.gif)


**代码：**
```python
# 前缀和解法
class Solution:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        ans = [0] * n
        for start, end, val in bookings:
            ans[start - 1] += val
            if end < n: ans[end] -= val
        for i in range(1, n):
            ans[i] += ans[i - 1]
        return ans
```

```python
# 扫描线解法
class Solution:
    def corpFlightBookings(self, bookings: List[List[int]], n: int) -> List[int]:
        ans = [0] * n
        d = dict()
        for start, end, val in bookings:
            d[start - 1] = d.get(start - 1, 0) + val
            d[end] = d.get(end, 0) - val
        s = 0
        for i in range(n):
            if i in d:
                s += d[i]
            ans[i] = s
        return ans
```


### [1110.删点成林](https://leetcode-cn.com/contest/weekly-contest-144/problems/delete-nodes-and-return-forest/)


**思路：**

深度优先搜索，在搜索的过程中检查当前结点是否需要删去，如果结点不需要删除，而它的父结点被删除，那么将它加入答案数组里。一遍DFS把所有操作做完，需要一些编程技巧，我们可以先从两边DFS入手，第一遍先标记需要加入答案数组的结点，即该结点不需要删除，而该结点的父结点需要删除，第二遍遍历答案数组，将答案数组中每棵树中需要删除的结点删除。然后我们可以考虑一遍DFS：如果当前结点是要被删除的，那么向上返回`None`，如果不需要被删除，则返回原结点，上层遍历左子树和右子树后，直接赋给这个返回值。还有一个优化就是把`to_delete`这个列表转换成集合，增加查询速度。


**代码：**
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
# 两遍DFS
class Solution:
    def delNodes(self, root: TreeNode, to_delete: List[int]) -> List[TreeNode]:
        if not root:
            return []
        self.ans = []
        
        def dfs(root, fd):
            if not root:
                return
            if root.val in to_delete:
                dfs(root.left, True)
                dfs(root.right, True)
            else:
                if fd:
                    self.ans.append(root)
                dfs(root.left, False)
                dfs(root.right, False)
            return
        
        def dfs_del(root):
            if not root:
                return
            if root.left and root.left.val in to_delete:
                root.left = None
            else:
                dfs_del(root.left)
            if root.right and root.right.val in to_delete:
                root.right = None
            else:
                dfs_del(root.right)
            return
        
        dfs(root, True)
        for node in self.ans:
            dfs_del(node)
        return self.ans
```

```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None
# 优化后的一遍DFS
class Solution:
    def delNodes(self, root: TreeNode, to_delete: List[int]) -> List[TreeNode]:
        s = set(to_delete)
        ans = []

        def dfs(root, flg):
            if not root: return None
            deleted = root.val in s
            if flg and not deleted:
                ans.append(root)
            root.left = dfs(root.left, deleted)
            root.right = dfs(root.right, deleted)
            return None if deleted else root
        dfs(root, True)
        return ans
```


### [1111.有效括号的嵌套深度](https://leetcode-cn.com/contest/weekly-contest-144/problems/maximum-nesting-depth-of-two-valid-parentheses-strings/)


**思路：**

本题标注难度虽然为`Hard`，但是对于熟悉括号匹配的同学来说，迅速想到解法并不难。括号匹配用到栈结构，遇到左括号`(`入栈，遇到右括号`)`出栈，栈的深度就是当前括号的深度。想要把括号字符串分为两个序列，并让他们的最大深度尽量小，那么我们只需要开两个栈，在入栈的过程中，尽量保持两个栈的深度相等即可，需要点技巧的地方在于入栈时候记录一下进入的是哪个栈，当然也可以用一个元素带标记的栈来实现。

如果深入分析括号位置的奇偶性，我们还可以总结出更简单的规则：我们观察一下字符串`"(((())))"`，先是一段连续的入栈，那么根据我们的入栈原则，肯定是奇数位置进入栈`1`，偶数位置进入栈`2`，那么当字符串不是连续入栈的情况呢？答案是每出栈一次就改变了一次入栈的奇偶性，如果入栈次序是`1-2-1-2`，这时有一个出栈，那么下一次出栈的顺序就倒过来从`2`开始出，同时也改变入栈奇偶性，下一次入栈就从`2`入，如果连续两个出栈，那么奇偶性就不变，下次入栈继续从`1`入。这样，利用按位与判断位置的奇偶性，用字符是否为`(`判断入栈的奇偶性是否改变，两者进行异或操作就得到了答案。


**代码：**
```python
class Solution:
    def maxDepthAfterSplit(self, seq: str) -> List[int]:
        flg = []
        s1 = []
        s2 = []
        ans = []
        for c in seq:
            if c == '(':
                if len(s1) <= len(s2):
                    s1.append(c)
                    ans.append(0)
                    flg.append(0)
                else:
                    s2.append(c)
                    ans.append(1)
                    flg.append(1)
            else:
                f = flg.pop()
                if f == 0:
                    ans.append(0)
                    s1.pop()
                else:
                    ans.append(1)
                    s2.pop()
        return ans
```

```python
# 一行写法 by lee215
class Solution:
    def maxDepthAfterSplit(self, seq: str) -> List[int]:
        return [i & 1 ^ (c == '(') for i, c in enumerate(seq)]
```


