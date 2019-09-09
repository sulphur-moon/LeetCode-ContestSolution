## [第 8 场双周赛](https://leetcode-cn.com/contest/biweekly-contest-8)

本周比赛考察了排列组合、字符串处理、动态规划、数学等算法。

### [1180. 统计只含单一字母的子串](https://leetcode-cn.com/contest/biweekly-contest-8/problems/count-substrings-with-only-one-distinct-letter)

**思路：**

统计一下每个字符连续出现区间的长度，然后根据等差数列求和公式计算这个区间有多少子串。处理字符串时，为了统一计算方式，可以在字符串结尾增加一个特殊标记来多分割出一个区间。


**代码：**
```python
class Solution:
    def countLetters(self, S: str) -> int:
        S += '#'
        ans, cnt, n = 0, 1, len(S)
        for i in range(1, n):
            if S[i] == S[i - 1]:
                cnt += 1
            else:
                ans += cnt * (cnt + 1) // 2
                cnt = 1
        return ans
```


### [1181. 前后拼接](https://leetcode-cn.com/contest/biweekly-contest-8/problems/before-and-after-puzzle)

**思路：**

本题直接根据题意进行字符串处理即可，主要就是考察一些字符串的处理技巧。为了不重复处理字符串的第一个单词和最后一个单词，可以先将所有字符串预处理，然后再用一个双重循环将符合答案的字符串拼接加入集合中，最后不要忘了按字典排序返回答案。


**代码：**
```python
class Solution:
    def beforeAndAfterPuzzles(self, phrases: List[str]) -> List[str]:
        ans = set()
        words = []
        for p in phrases:
            words.append(p.split(' '))
        n = len(phrases)
        for i in range(n):
            for j in range(n):
                if i != j and words[i][-1] == words[j][0]:
                    t = words[i][:-1] + words[j]
                    ans.add(' '.join(t))
        return sorted(list(ans))
```
### [1182. 与目标颜色间的最短距离](https://leetcode-cn.com/contest/biweekly-contest-8/problems/shortest-distance-to-target-color)

**思路：**

先枚举每种颜色，然后分别正序和倒序扫描数组，求每个位置到当前目标颜色的距离最小值。具体做法是：

1. 初始值 left 和 right 都为 -1（设为正无穷更方便些）；
2. 如果当前位置颜色刚好是目标颜色，那么距离就为 0，并更新 left 或 right 为 0；
3. 如果当前位置颜色不等于目标颜色，那么就看 left 是否不为 -1。如果不为 -1，说明左边存在目标颜色，并且最近的距离为 left + 1，更新答案；
4. 右边同理。


**代码：**
```python
class Solution:
    def shortestDistanceColor(self, colors: List[int], queries: List[List[int]]) -> List[int]:
        n = len(colors)
        d = [[-1] * 4 for _ in range(n)]
        for c in range(1, 4):
            left, right = -1, -1
            for i in range(n):
                if colors[i] == c:
                    left = 0
                    d[i][c] = 0
                elif left != -1:
                    left += 1
                    if d[i][c] == -1:
                        d[i][c] = left
                    else:
                        d[i][c] = min(d[i][c], left)
                if colors[n - i - 1] == c:
                    right = 0
                    d[n - i - 1][c] = 0
                elif right != -1:
                    right += 1
                    if d[n - i - 1][c] == -1:
                        d[n - i - 1][c] = right
                    else:
                        d[n - i - 1][c] = min(d[n - i - 1][c], right)
        ans = []
        for i, c in queries:
            ans.append(d[i][c])
        return ans
```


### [1183. 矩阵中 1 的最大数量](https://leetcode-cn.com/contest/biweekly-contest-8/problems/maximum-number-of-ones)

**思路：**

这是一道数学题。首先我们可以知道，正方形子矩阵在覆盖整个矩阵的时候，一定是循环出现的。那么我们就要看正方形子矩阵中，那些元素出现的次数最多即可。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1183-1.png)

如图所示，用矩阵的宽和高分别除以正方形子矩阵的边长，得到的商和余数分别为 `d1, m1, d2, m2`。可以看出，重复次数最多的部分就是红色部分，面积为 `m1 * m2`， 重复的次数为 `(d1 + 1) * (d2 + 1)` ，所以 `maxOnes` 应该首先填满红色部分。如果还有剩余，我们要比较黄色部分重复的次数 `(d1 + 1) * d2` 多还是绿色部分重复的次数 `(d2 + 1) * d1` 多。重复次数多的优先填满，如果 `maxOnes` 还有剩余再填满次数少的。如果红色、黄色、绿色区域都被填满，那么剩余的 `maxOnes` 就重复 `d1 * d2` 次。


**代码：**
```python
class Solution:
    def maximumNumberOfOnes(self, width: int, height: int, sideLength: int, maxOnes: int) -> int:
        d1, m1 = divmod(width, sideLength)
        d2, m2 = divmod(height, sideLength)
        ans = 0
        t = m1 * m2
        if maxOnes > t:
            maxOnes -= t
            ans += t * (d1 + 1) * (d2 + 1)
        else:
            return maxOnes * (d1 + 1) * (d2 + 1)
        if d1 * (d2 + 1) < d2 * (d1 + 1):
            d1, d2, m1, m2 = d2, d1, m2, m1
        t = (sideLength - m1) * m2
        if maxOnes > t:
            maxOnes -= t
            ans += t * d1 * (d2 + 1)
        else:
            return ans + maxOnes * d1 * (d2 + 1)
        t = (sideLength - m2) * m1
        if maxOnes > t:
            maxOnes -= t
            ans += t * d2 * (d1 + 1)
        else:
            return ans + maxOnes * d2 * (d1 + 1)
        return ans + maxOnes * d1 * d2
```


