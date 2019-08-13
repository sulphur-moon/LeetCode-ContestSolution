## [第 149 场周赛](https://leetcode-cn.com/contest/weekly-contest-149)

本周比赛题目很考察编程技巧，最后一题比较难，存在多种解法。本周用到的算法有数学方法、动态规划、线段树等。

### [1154. 一年中的第几天](https://leetcode-cn.com/contest/weekly-contest-149/problems/ordinal-number-of-date)

**思路：**

先处理字符串，提取年（year）、月（month）和日（day）。如果月份为第一月，那么直接返回 `day` 即可。如果月份为第二月，那么直接返回 `day + 31`。如果月份大于二月，那么先判断是否为闰年，如果为闰年，结果就加 29，如果不为闰年，则结果加28。然后遍历所有小于该月的月份，统计大月（31天）和小月（30）天的个数，最后相加输出答案。


**代码：**
```python
class Solution:
    def ordinalOfDate(self, date: str) -> int:
        month_of_days31 = [1, 3, 5, 7, 8, 10, 12]
        month_of_days30 = [4, 6, 9, 11]
        feb_month = 2
        year, month, day = map(int, date.split('-'))
        
        def is_leap_year(year):
            if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
                return True
            return False
        
        if month == 1:
            return day

        if month == 2:
            return day + 31

        days_of_31_num = 0
        days_of_30_num = 0
        
        # 31天月份数
        for days_of_31 in month_of_days31:
            if days_of_31 < month:
                days_of_31_num += 1
            else:
                break

        # 30天月份数
        for days_of_30 in month_of_days30:
            if days_of_30 < month:
                days_of_30_num += 1
            else:
                break

        return days_of_31_num * 31 + days_of_30_num * 30 + (29 if is_leap_year(year) else 28) + day
```


### [1155. 掷骰子的N种方法](https://leetcode-cn.com/contest/weekly-contest-149/problems/number-of-dice-rolls-with-target-sum)

**思路：**

按照题意，这道题目可以看做一个背包问题，用动态规划解决。用 `dp[i][j]` 表示 `i` 个骰子掷出 `j` 点的方案数目。状态转移方程为 `dp[i][j] = dp[i][j] + dp[i - 1][j - k]  (1 <= k <= f)`。代码实现可以用递推或者记忆化搜索。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1155-1.png)


**代码：**

递归 + 记忆化搜索

```python
class Solution:
    def __init__(self):
        self.memo = {}
        self.m = 10 ** 9 + 7
    def numRollsToTarget(self, d: int, f: int, target: int) -> int:
        if (d, f, target) in self.memo:
            return self.memo[(d, f, target)]
        if target <= 0:
            return 0
        if d == 1 and target <= f:
            return 1
        if d == 1 and target > f:
            return 0
        
        ans = 0
        for i in range(1, f + 1):
            ans += self.numRollsToTarget(d - 1, f, target - i)
        ans = ans % self.m
        self.memo[(d, f, target)] = ans
        return ans
```

递推 + 动态规划

```python
class Solution:
    def numRollsToTarget(self, d: int, f: int, target: int) -> int:
        m = 10 ** 9 + 7
        dp = [[0] * (target + 1) for _ in range(d + 1)]
        dp[0][0] = 1
        for i in range(1, d + 1):
            for j in range(1, f + 1):
                for k in range(j, target + 1):
                    dp[i][k] = (dp[i][k] + dp[i - 1][k - j]) % m
        return dp[d][target]
```


### [1156. 单字符重复子串的最大长度](https://leetcode-cn.com/contest/weekly-contest-149/problems/swap-for-maximum-repeated-substring)

**思路：**

先统计字符串中每个字符出现的次数，用 `left[i]` 表示位置 `i` 左侧连续相等字符的最大长度，用 `right[i]` 表示位置 `i` 右侧连续相等字符的最大长度，分别自左向右和自右向左扫描一次，求得 `left[i]` 和 `right[i]`。

由于最多只允许交换一次字符，我们可以遍历一次求得答案。当我们遍历位置 `i` 时，分两种情况讨论：

1. 当位置 `i` 两侧的字符相等时，我们查看 `left[i] + right[i]` 是否小于该字符出现的次数：如果小于，那么说明有其他位置的该字符可以交换到 `i` 位置，将左右两边连续的字符连接起来，形成长度为 `left[i] + right[i] + 1` 的连续字符，亦或是多的那个字符本身就在 `i` 位置，我们无需做任何操作。如果等于，那么我们可以将右侧连续字符的最后一个字符交换到 `i` 位置，或者把左侧连续字符的第一个字符交换到 `i` 位置，形成长度为 `left[i] + right[i]` 的连续字符。
2. 当位置 `i` 两侧的字符不相等时，我们分别查看 `left[i]` 和 `right[i]` 是否小于各自字符出现的次数：如果小于，则用 `left[i] + 1` 或 `right[i] + 1` 更新答案；如果等于，则直接用 `left[i]` 和 `right[i]` 更新答案。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1156-1.png)


**代码：**
```python
class Solution:
    def maxRepOpt1(self, text: str) -> int:
        ans, n = 1, len(text)
        # 统计每个字母出现的次数
        cnt = collections.Counter(text)
        # 统计两边连续的字母最大长度
        left, right = [1] * n, [1] * n
        left[0], right[n - 1] = 0, 0
        for i in range(2, n):
            if text[i - 1] == text[i - 2]:
                left[i] = left[i - 1] + 1
        for i in range(n - 3, -1, -1):
            if text[i + 1] == text[i + 2]:
                right[i] = right[i + 1] + 1
        # 遍历空位
        for i in range(n):
            c = cnt[text[i + 1]] if i == 0 else cnt[text[i - 1]]
            # 如果空位两侧字符一样
            if i == 0 or i == n - 1 or text[i - 1] == text[i + 1]:
                # 如果有多余同样的字符可以填入空位中
                if left[i] + right[i] < c:
                    ans = max(ans, left[i] + right[i] + 1)
                # 没有多余字符
                elif left[i] + right[i] == c:
                    ans = max(ans, c)
            # 用单侧连续字符更新答案
            else:
                ans = max(ans, left[i] + 1) if left[i] < c else max(ans, left[i])
                ans = max(ans, right[i] + 1) if right[i] < c else max(ans, right[i])
        return ans
```


### [1157. 子数组中占绝大多数的元素](https://leetcode-cn.com/contest/weekly-contest-149/problems/online-majority-element-in-subarray)

**思路：**

暴力的方法可以直接统计或者使用摩尔投票法。但是对于查询次数最多为 `10000` 的情况会超时。

优化的方法有很多，比如分桶或者使用线段树。这里介绍一个可以通过测试，并且编程复杂度比较小的方法。把每个值的索引加入一个列表，然后用二分搜索查询 `left` 和 `right` 插入的位置，通过比较 `right - left `是否大于等于 `threshold`。由于要查询绝对众数，我们可以将数组中数字按照频率排序，然后进行遍历，这样就可以保证绝对众数被最先搜索到。


**代码：**
```python
class MajorityChecker:

    def __init__(self, arr: List[int]):
        self.d = collections.defaultdict(list)
        for index, value in enumerate(arr):
            self.d[value].append(index)
        self.freq = sorted([(len(locations), value) for value, locations in self.d.items()], reverse = True)

    def query(self, left: int, right: int, threshold: int) -> int:
        for f, v in self.freq:
            if f < threshold: break
            locations = self.d[v]
            low = bisect.bisect_left(locations, left)
            high = bisect.bisect_right(locations, right)
            if high - low >= threshold:
                return v
        return -1


# Your MajorityChecker object will be instantiated and called as such:
# obj = MajorityChecker(arr)
# param_1 = obj.query(left,right,threshold)
```


