## [第 4 场双周赛](https://leetcode-cn.com/contest/biweekly-contest-4)

本周比赛比较简单，用到算法有数学方法、字符串处理、深度优先搜索、贪心等。

### [1118. 一月有多少天](https://leetcode-cn.com/contest/biweekly-contest-4/problems/number-of-days-in-a-month)

**思路：**

本题比较简单，只需要掌握判断语句和闰年的计算方法即可。闰年规定如下：

1. 普通年能被4整除且不能被100整除的为闰年。
2. 世纪年能被400整除的是闰年。

另外还有公元前闰年计算和数值很大年份的闰年计算规则，但是本题的数据范围为`1583 <= Y <= 2100`，所以只需要用基本规则即可。

月份的天数规律是：大月31天，小月30天。有一个口诀是“七前单大，八后双大”，即七月份之前的奇数月份（1、3、5、7）是31天，八月份以后的偶数月份（8、10、12）是31天。在程序中，我们直接可以用一个hash表保存，然后直接查询就可以了。

程序的过程是先判断月份是否为2月，如果是，则判断是否为闰年，闰年返回29，非闰年返回28。如果月份不是2月，那么判断是否为大月，如果是则返回31，不是则返回30。


**代码：**
```python
class Solution:
    def numberOfDays(self, Y: int, M: int) -> int:
        big = {1, 3, 5, 7, 8, 10, 12}
        if M == 2:
            if (Y % 4) == 0:
                if (Y % 100) == 0:
                    if (Y % 400) == 0:
                        return 29
                    else:
                        return 28
                else:
                    return 29
            return 28
        else:
            if M in big:
                return 31
            else:
                return 30
```


### [1119. 删去字符串中的元音](https://leetcode-cn.com/contest/biweekly-contest-4/problems/remove-vowels-from-a-string)

**思路：**

把五个元音建一个哈希表，遍历字符串中每个字符，如果字符不在哈希表中，则加入答案数组，最后返回连接答案数组的字符串。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1119-1.gif)

**代码：**
```python
class Solution:
    def removeVowels(self, S: str) -> str:
        y = {'a','e','i','o','u'}
        ans = []
        for c in S:
            if c not in y:
                ans.append(c)
        return ''.join(ans)
```


### [1120. 子树的最大平均值](https://leetcode-cn.com/contest/biweekly-contest-4/problems/maximum-average-subtree)

**思路：**

深度优先搜索，返回值的设计需要点技巧，每次返回以当前结点为根的子树结点个数`num`和子树所有结点的和`val`，那么当前结点的子树的平均值就是`val/num`，每次用平均值更新答案，并把`num`和`val`返回给上一层，上一层结点就可以利用这个返回值进行计算了。


**代码：**
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Solution:
    def maximumAverageSubtree(self, root: TreeNode) -> float:
        self.ans = 0
        
        def dfs(root):
            if not root:
                return 0, 0
            ln, lv = dfs(root.left)
            rn, rv = dfs(root.right)
            num = ln + rn + 1
            val = lv + rv + root.val
            self.ans = max(self.ans, val/num)
            return num, val
        
        dfs(root)
        return self.ans
            
```


### [1121. 将数组分成几个递增序列](https://leetcode-cn.com/contest/biweekly-contest-4/problems/divide-array-into-increasing-sequences)

**思路：**

本题可以直接猜出一个数学结论，设`m`为`nums`数组中众数的频率，那么当且仅当`m * K <= len(nums)`时返回`True`，否则返回`False`。

以样例输入为例：

1. `nums = [1,2,2,3,3,4,4], K = 3`，众数是`2`，众数频率`m=2`，那么我们先要把数字`2`分到两个子序列里，即`[2], [2]`，因为子序列是严格递增的，相同的数字显然不能分到同一个子序列里。接下来把其他数字填进去，`1`填进第一个子序列中，结果变为`[1, 2], [2]`，然后`3`和`4`都每个子序列中各填一个。这样只要`m * K <= len(nums)`，先把众数分到`m`个子序列中，那么剩下的数字肯定是可以满足每个子序列长度都大于等于`K`，且没有重复数字的。
2. `nums = [5,6,6,7,8], K = 3`，众数是`6`，众数频率`m=2`，那么我们先要把数字`2`分到两个子序列里，即`[6], [6]`，那么剩下的3个数`5, 7, 8`无论怎么分，都不会让所有子序列长度都大于等于`K`。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1121-1.gif)

**代码：**
```python
class Solution:
    def canDivideIntoSubsequences(self, nums: List[int], K: int) -> bool:
        cnt = collections.Counter(nums)
        m = cnt.most_common(1)[0][1]
        return m * K <= len(nums)
```


