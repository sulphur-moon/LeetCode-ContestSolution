## Weekly Contest 143 Solution

本周比赛难度适中，考察内容比较全面，有简单的遍历，需要找规律的数学方法，需要点变成技巧的动态规划算法和字符串处理题。

### [1103. 分糖果 II](https://leetcode-cn.com/contest/weekly-contest-143/problems/distribute-candies-to-people/)

排排坐，分糖果。

我们买了一些糖果 `candies`，打算把它们分给排好队的 **n = num_people** 个小朋友。

给第一个小朋友 1 颗糖果，第二个小朋友 2 颗，依此类推，直到给最后一个小朋友 `n` 颗糖果。

然后，我们再回到队伍的起点，给第一个小朋友 `n + 1` 颗糖果，第二个小朋友 `n + 2` 颗，依此类推，直到给最后一个小朋友 `2 * n` 颗糖果。

重复上述过程（每次都比上一次多给出一颗糖果，当到达队伍终点后再次从队伍起点开始），直到我们分完所有的糖果。注意，就算我们手中的剩下糖果数不够（不比前一次发出的糖果多），这些糖果也会全部发给当前的小朋友。

返回一个长度为 `num_people`、元素之和为 `candies` 的数组，以表示糖果的最终分发情况（即 `ans[i]` 表示第 `i` 个小朋友分到的糖果数）。

**示例 1：**

```
输入：candies = 7, num_people = 4
输出：[1,2,3,1]
解释：
第一次，ans[0] += 1，数组变为 [1,0,0,0]。
第二次，ans[1] += 2，数组变为 [1,2,0,0]。
第三次，ans[2] += 3，数组变为 [1,2,3,0]。
第四次，ans[3] += 1（因为此时只剩下 1 颗糖果），最终数组变为 [1,2,3,1]。
```

**示例 2：**

```
输入：candies = 10, num_people = 3
输出：[5,2,3]
解释：
第一次，ans[0] += 1，数组变为 [1,0,0]。
第二次，ans[1] += 2，数组变为 [1,2,0]。
第三次，ans[2] += 3，数组变为 [1,2,3]。
第四次，ans[0] += 4，最终数组变为 [5,2,3]。
```

**提示：**

- `1 <= candies <= 10^9`
- `1 <= num_people <= 1000`

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

在一棵无限的二叉树上，每个节点都有两个子节点，树中的节点 **逐行** 依次按 “之” 字形进行标记。

如下图所示，在奇数行（即，第一行、第三行、第五行……）中，按从左到右的顺序进行标记；

而偶数行（即，第二行、第四行、第六行……）中，按从右到左的顺序进行标记。

![img](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2019/06/28/tree.png)

给你树上某一个节点的标号 `label`，请你返回从根节点到该标号为 `label` 节点的路径，该路径是由途经的节点标号所组成的。

**示例 1：**

```
输入：label = 14
输出：[1,3,4,14]
```

**示例 2：**

```
输入：label = 26
输出：[1,2,6,10,26]
```

**提示：**

- `1 <= label <= 10^6`

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

附近的家居城促销，你买回了一直心仪的可调节书架，打算把自己的书都整理到新的书架上。

你把要摆放的书 `books` 都整理好，叠成一摞：从上往下，第 `i` 本书的厚度为 `books[i][0]`，高度为 `books[i][1]`。

**按顺序** 将这些书摆放到总宽度为 `shelf_width` 的书架上。

先选几本书放在书架上（它们的厚度之和小于等于书架的宽度 `shelf_width`），然后再建一层书架。重复这个过程，直到把所有的书都放在书架上。

需要注意的是，在上述过程的每个步骤中，**摆放书的顺序与你整理好的顺序相同**。 例如，如果这里有 5 本书，那么可能的一种摆放情况是：第一和第二本书放在第一层书架上，第三本书放在第二层书架上，第四和第五本书放在最后一层书架上。

每一层所摆放的书的最大高度就是这一层书架的层高，书架整体的高度为各层高之和。

以这种方式布置书架，返回书架整体可能的最小高度。

**示例：**

![img](https://assets.leetcode-cn.com/aliyun-lc-upload/uploads/2019/06/28/shelves.png)

```
输入：books = [[1,1],[2,3],[2,3],[1,1],[1,1],[1,1],[1,2]], shelf_width = 4
输出：6
解释：
3 层书架的高度和为 1 + 3 + 2 = 6 。
第 2 本书不必放在第一层书架上。
```

**提示：**

- `1 <= books.length <= 1000`
- `1 <= books[i][0] <= shelf_width <= 1000`
- `1 <= books[i][1] <= 1000`

**思路：**

动态规划。用`dp[i]`表示放置前`i`本书所需要的书架最大高度，初始值`dp[0] = 0`，其他为最大值`1000*1000`。遍历每一本书，把当前这本书作为书架最后一层的最后一本书，将这本书之前的书向后调整，看看是否可以减少之前的书架高度。状态转移方程为`dp[i] = min(dp[i], dp[j - 1] + h)`，其中`j`表示最后一层所能容下书籍的索引，`h`表示最后一层最大高度。

**图解：**

![图解](https://github.com/sulphur-moon/LeetCode-ContestSolution/blob/master/LeetCode%20Contest%20Solutions/pics/143-3.gif?raw=true)

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

给你一个以字符串形式表述的 [布尔表达式](https://baike.baidu.com/item/布尔表达式/1574380?fr=aladdin)（boolean） `expression`，返回该式的运算结果。

有效的表达式需遵循以下约定：

- `"t"`，运算结果为 `True`
- `"f"`，运算结果为 `False`
- `"!(expr)"`，运算过程为对内部表达式 `expr` 进行逻辑 **非的运算**（NOT）
- `"&(expr1,expr2,...)"`，运算过程为对 2 个或以上内部表达式 `expr1, expr2, ...` 进行逻辑 **与的运算**（AND）
- `"|(expr1,expr2,...)"`，运算过程为对 2 个或以上内部表达式 `expr1, expr2, ...` 进行逻辑 **或的运算**（OR）

**示例 1：**

```
输入：expression = "!(f)"
输出：true
```

**示例 2：**

```
输入：expression = "|(f,t)"
输出：true
```

**示例 3：**

```
输入：expression = "&(t,f)"
输出：false
```

**示例 4：**

```
输入：expression = "|(&(t,f,t),!(t))"
输出：false
```

**提示：**

- `1 <= expression.length <= 20000`
- `expression[i]` 由 `{'(', ')', '&', '|', '!', 't', 'f', ','}` 中的字符组成。
- `expression` 是以上述形式给出的有效表达式，表示一个布尔值。

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
