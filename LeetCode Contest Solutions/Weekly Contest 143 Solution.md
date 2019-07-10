## Weekly Contest 143 Solution

本周比赛难度适中，考察内容比较全面，有简单的遍历，需要找规律的数学方法，需要点变成技巧的动态规划算法和字符串处理题。

### [1103. 分糖果 II](https://leetcode-cn.com/contest/weekly-contest-143/problems/distribute-candies-to-people/)

**思路：**

直接模拟。开一个长度为`num_people`的数组，索引`i`从`0`开始遍历，第`i % num_people`个小朋友分得`i + 1`块糖，糖的总数相应减少`i + 1`。最后不足`i + 1`块糖都给最后一个小朋友。

**代码：**

```python
class Solution:
    def distributeCandies(self, candies: int, num_people: int) -> List[int]:
        ans = [0] * num_people
        i = 0
        while candies > i:
            ans[i % num_people] += i + 1
            candies -= i + 1
            i += 1
        ans[i % num_people] += candies
        return ans
```

### [1104. 二叉树寻路](https://leetcode-cn.com/contest/weekly-contest-143/problems/path-in-zigzag-labelled-binary-tree/)

**思路：**

寻找数学规律。我们将树种每个结点的原索引标记在结点下方，如图所示。我们会发现一个规律，在偶数行，原索引和逆序后的索引值加在一起，等于该行最小索引和最大索引的值（因为每一行都是一个等差数列），而这个值也恰好等于该行最小索引值的3倍减去1（因为下一行开始的索引是前一行开始索引的2倍）。如果我们按照原索引进行遍历，`label = 14`，那么我们需要做的操作就是每次取`label //= 2`，最终得到`[1, 3, 7, 14]`这样一个图中蓝色标记的路径，但是由于`label = 14`处于偶数行，所以逆序之后的路径是镜像的，我们就需要将路径中奇数的位置反过来，得到`[1, 3, 4, 14]`，即图中红色的路径。如果`label = 5`处于奇数行，那么我们遍历后得到`[1, 2, 5]`，由于其中偶数行是逆序的，我们就需要将路径中的偶数位置反过来，得到`[1, 3, 5]`，即图中绿色的路径。

![sol.png](https://pic.leetcode-cn.com/90a8db9885f824601ecb86b93f2ea5eaac36c8a80a678b3d589ff23b3a742d2d-sol.png)

**代码：**

```python
class Solution:
    def pathInZigZagTree(self, label: int) -> List[int]:
        if label == 1:
            return [1]
        ans = []
        while label > 0:
            ans.append(label)
            label //= 2
        ans = ans[::-1]
        base = 2
        n = len(ans)
        flg = n % 2
        for i in range(1, n):
            if i % 2 == flg:
                s = base * 3 - 1
                ans[i] = s - ans[i]
            base *= 2
        return ans
```

### [1105. 填充书架](https://leetcode-cn.com/contest/weekly-contest-143/problems/filling-bookcase-shelves/)

**思路：**

动态规划。用`dp[i]`表示放置前`i`本书所需要的书架最大高度，初始值`dp[0] = 0`，其他为最大值`1000*1000`。遍历每一本书，把当前这本书作为书架最后一层的最后一本书，将这本书之前的书向后调整，看看是否可以减少之前的书架高度。状态转移方程为`dp[i] = min(dp[i], dp[j - 1] + h)`，其中`j`表示最后一层所能容下书籍的索引，`h`表示最后一层最大高度。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1105-1.gif)

**代码：**

```python
class Solution:
    def minHeightShelves(self, books: List[List[int]], shelf_width: int) -> int:
        n = len(books)
        dp = [1000000] * (n + 1)
        dp[0] = 0
        for i in range(1, n + 1):
            tmp_width, j, h = 0, i, 0
            while j > 0:
                tmp_width += books[j - 1][0]
                if tmp_width > shelf_width:
                    break
                h = max(h, books[j - 1][1])
                dp[i] = min(dp[i], dp[j - 1] + h)
                j -= 1
        return dp[-1]
```

### [1106. 解析布尔表达式](https://leetcode-cn.com/contest/weekly-contest-143/problems/parsing-a-boolean-expression/)

**思路：**

本题正常做法应该用栈或者递归，记录每一层的运算符，运算后的结果返回给上一层。不过在Python中，我们可以有个偷懒的办法，利用`eval()`函数来帮我们计算布尔表达式的值。在遍历表达式的过程中，我们还是需要一个变量`level`来记录当前是第几层表达式，每当遇到左括号`(`，`level`就加1，遇到右括号`)`，`level`就减一。遇到运算符`!`、`&`或`|`时，我们将其替换为Python中的`not`、`and`和`or`，并记录下来，遇到该层内的逗号`,`时，我们就把逗号替换成该层的运算符。遇到`f`替换为`False`，遇到`t`替换为`True`。最后用`eval()`函数计算整个替换后的表达式。

**代码：**

```python
class Solution:
    def parseBoolExpr(self, expression: str) -> bool:
        level = 0
        sign = [""]
        exp = []
        for e in expression:
            if e == "!":
                sign[level] = " not "
                exp.append(" not ")
            if e == "&":
                sign[level] = " and "
            if e == "|":
                sign[level] = " or "
            if e == "(":
                sign.append("")
                level += 1
                exp.append("(")
            if e == ")":
                level -= 1
                exp.append(")")
            if e == ",":
                exp.append(sign[level - 1])
            if e == "f":
                exp.append("False")
            if e == "t":
                exp.append("True")
        return eval(''.join(exp))
```
