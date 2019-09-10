## [第 153 场周赛](https://leetcode-cn.com/contest/weekly-contest-153)

本周比赛考察了数组遍历求和、基姆拉尔森计算公式、动态规划等算法。

### [1184. 公交站间的距离](https://leetcode-cn.com/contest/weekly-contest-153/problems/distance-between-bus-stops)

**思路：**

从 `start` 到 `destination` 遍历数组，并累计距离，然后和另外一边进行比较，取较小者。用前缀和实现比较方便。


**代码：**
```python
class Solution:
    def distanceBetweenBusStops(self, distance: List[int], start: int, destination: int) -> int:
        d = [0]
        for i in distance:
            d.append(d[-1] + i)
        if start > destination:
            start, destination = destination, start
        t = d[destination] - d[start]
        return min(t, d[-1] - t)
```


### [1185. 一周中的第几天](https://leetcode-cn.com/contest/weekly-contest-153/problems/day-of-the-week)

**思路：**

首先可以根据 `1971` 年第一天是星期几推算给定的日期是星期几，中间要判断闰年。偷懒的办法是调用库函数。还有一种数学方法是基姆拉尔森计算公式（Kim Larsen Calculation Formula），可以直接计算出给定日期是星期几。


**代码：**

利用库函数

```python
import time, datetime

class Solution:
    def dayOfTheWeek(self, day: int, month: int, year: int) -> str:
        weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        d = datetime.datetime(year, month, day)
        return weekday[d.weekday()]
```

基姆拉尔森计算公式

```python
class Solution:
    def dayOfTheWeek(self, day: int, month: int, year: int) -> str:
        weekday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if month < 3:
            month += 12
            year -= 1
        w = (year + year // 4 + year // 400 - year // 100 + 2 * month + 3 * (month + 1) // 5 + day) % 7
        return weekday[w]
```


### [1186. 删除一次得到子数组最大和](https://leetcode-cn.com/contest/weekly-contest-153/problems/maximum-subarray-sum-with-one-deletion)

**思路：**

动态规划，用 `dp[i][0]` 表示以 `arr[i - 1]` 结尾的未删去元素的最大子数组和，用 `dp[i][1]` 表示以 `arr[i - 1]` 结尾的删去一个元素的最大子数组和。状态转移方程为：

1. 对于 `dp[i][0]`，我们有两种选择，一种是累加  `arr[i - 1]` ，另一种是从 `arr[i - 1]` 重新开始；
2. 对于 `dp[i][1]`，我们也有两种选择，一种是删去 `arr[i - 1]` 即 `dp[i - 1][0]`，另一种是保留 `arr[i - 1]` 即`dp[i - 1][1] + arr[i - 1] `。


**代码：**
```python
class Solution:
    def maximumSum(self, arr: List[int]) -> int:
        dp = [[-10000 for _ in range(2)] for _ in range(len(arr) + 1)]
        ans = -10000
        for i in range(1, len(arr) + 1):
            dp[i][0] = max(dp[i-1][0] + arr[i-1], arr[i-1])
            dp[i][1] = max(dp[i-1][0], dp[i-1][1] + arr[i-1])
            ans = max(ans, max(dp[i][0], dp[i][1]))
        return ans
```


### [1187. 使数组严格递增](https://leetcode-cn.com/contest/weekly-contest-153/problems/make-array-strictly-increasing)

**思路：**

此题有多种动态规划设计思路，这里介绍其中一种。

1. 将 `arr2` 去重排序，得到一个严格递增的序列；
2. 遍历 `arr1`，用 `dp[a]` 表示当前位置元素为 `a` 时，所需替换的最小操作数；
3. 由上个 `dp` 向下一步 `dp` 转移时，遍历前一个元素的所有可能性 `x`；
4. 当上一个元素小于当前元素时候，我们可以不用替换当前元素，继承上一个元素 `x` 的状态，并在这些状态中取操作数最小的那一个；
5. 不管上一个元素 `x` 是否小于当前元素，我们都可以把当前元素在 `arr2` 中选一个尽量小的元素替换，以方便后续构造，所以要在 `arr2` 中二分查找第一个大于上一个元素 `x` 的元素，进行替换，此时操作数要比上一个状态的操作数加 1。


**代码：**
```python
class Solution:
    def makeArrayIncreasing(self, arr1: List[int], arr2: List[int]) -> int:
        arr2 = sorted(set(arr2))
        dp = { -1 : 0 }
        for a in arr1:
            t = { }
            for x, d in dp.items():
                if a > x:
                    t[a] = min(t.get(a, float('inf')), d)
                i = bisect.bisect_right(arr2, x)
                if i < len(arr2):
                    t[arr2[i]] = min(t.get(arr2[i], float('inf')), d + 1)
            dp = t
        return -1 if not dp else min(dp.values())
```


