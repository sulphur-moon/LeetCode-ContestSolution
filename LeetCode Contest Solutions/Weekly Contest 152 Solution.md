## [第 152 场周赛](https://leetcode-cn.com/contest/weekly-contest-152)

本周比赛考察了排列组合、滑动窗口、数学统计、bitmap、哈希等算法。

### [1175. 质数排列](https://leetcode-cn.com/contest/weekly-contest-152/problems/prime-arrangements)

**思路：**

题目意思就是，对于输入的正整数 `n`，小于等于 `n` 的质数取全排列，小于等于 `n` 的合数取全排列，在根据乘法原理相乘取模。由于小于 `100` 的质数只有 25 个，我们可以把这些质数列出来，在从 `1` 到 `n` 遍历的过程中判断质数，把质数和合数分别计数，并计算全排列数。


**代码：**
```python
class Solution:
    def numPrimeArrangements(self, n: int) -> int:
        mod = 10 ** 9 + 7
        primes = set([2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97])
        cnt1, cnt2, ans = 0, 0, 1
        for i in range(1, n + 1):
            if i in primes:
                cnt1 += 1
                ans *= cnt1
            else:
                cnt2 += 1
                ans *= cnt2
        return ans % mod
```


### [1176. 健身计划评估](https://leetcode-cn.com/contest/weekly-contest-152/problems/diet-plan-performance)

**思路：**

因为要计算每连续 `k` 天的消耗总卡路里，所以我们采取滑动窗口的方法计算。这里有个编程小技巧，类似于链表中的哑结点，可以在 `calories` 前插入一个 `0` 元素（或者在最后插入也可以），这样可以做到后面用一套代码判断每个窗口。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1176-1.gif)


**代码：**
```python
class Solution:
    def dietPlanPerformance(self, calories: List[int], k: int, lower: int, upper: int) -> int:
        calories.insert(0, 0)
        ans, n, s = 0, len(calories), sum(calories[:k])
        for i in range(k, n):
            s += calories[i] - calories[i - k]
            if s > upper:
                ans += 1
            if s < lower:
                ans -= 1
        return ans
```


### [1177. 构建回文串检测](https://leetcode-cn.com/contest/weekly-contest-152/problems/can-make-palindrome-from-substring)

**思路：**

统计区间中每个字符出现的次数，如果一个字符出现偶数次，那么显然可以把这个字符都调整到字符串的对称位置，这样就不需要进行替换的开销。如果有 `odd` 个字符出现次数为奇数次，我们分类讨论：

1. 如果 `odd` 为奇数，那么说明子字符串长度为奇数，然后选择任意一个出现次数为奇数的字符，将它放在子字符串的中间位置，剩下的该字符分别放置在对称位置，剩余的 `odd - 1` 种出现次数为奇数次的字符，需要进行 `(odd - 1) // 2 = odd // 2` 次替换，如果这个数字小于等于 `k`，那么这个子字符串是可以变成回文串的，否则不能变为回文串。
2. 如果 `odd` 为偶数，那么说明子字符串长度为偶数，然后将这 `odd` 种出现次数为奇数次的字符进行 `odd // 2` 次替换，如果这个数字小于等于 `k`，那么这个子字符串是可以变成回文串的，否则不能变为回文串。

为了快速求解某个区间中每个字符出现的次数，我们可以用前缀和的思想， `cnt[i][j]` 表示字符 `j` 在子串 `s[:i]` 中出现的次数。


**代码：**
```python
class Solution:
    def canMakePaliQueries(self, s: str, queries: List[List[int]]) -> List[bool]:
        ans = []
        n = len(s)
        cnt = [[0] * 26 for _ in range(n + 1)]
        for i in range(n):
            for j in range(26):
                cnt[i + 1][j] = cnt[i][j]
            cnt[i + 1][ord(s[i]) - 97] += 1
        for left, right, k in queries:
            odd = 0
            for i in range(26):
                if (cnt[right + 1][i] - cnt[left][i]) % 2 == 1:
                    odd += 1
            ans.append(k >= odd // 2)
        return ans
```


### [1178. 猜字谜](https://leetcode-cn.com/contest/weekly-contest-152/problems/number-of-valid-words-for-each-puzzle)

**思路：**

根据题意，先把 `words` 中每一个单词看成一个字符集合，然后统计一下相同字符集合的个数，可以用 bitmap 实现，在 python 中，我们可以用 `frozenset()` 来实现。接下来根据字谜 `puzzles` 来寻找谜底，这里有个陷阱，如果直接根据题目描述实现，遍历每个谜底的集合，检查是否符合要求，就会超时，因为谜底的个数可能达到 `10^5`。我们观察到谜面 `puzzles[i]` 的长度固定为 7，而且第一个字母是一定要包含的，所以我们可以从谜面枚举可能的谜底，再根据 `Counter` 计数累加，这样枚举的次数为 `2^6 = 64 < 10^5`，大大减少时间复杂度。


**代码：**

```python
from itertools import combinations as cb
class Solution:
    def findNumOfValidWords(self, words: List[str], puzzles: List[str]) -> List[int]:
        cnt = collections.Counter([frozenset(w) for w in words])
        return [sum(cnt[frozenset(s + (p[0], ))] for l in range(len(p)) for s in cb(p[1:], l)) for p in puzzles]
```


