## [第 6 场双周赛](https://leetcode-cn.com/contest/biweekly-contest-6)

本场双周赛比较简单，用到算法有统计、前缀和、滑动窗口、枚举、深度优先搜索、图论等。

### [1150. 检查一个数是否在数组中占绝大多数](https://leetcode-cn.com/contest/biweekly-contest-6/problems/check-if-a-number-is-majority-element-in-a-sorted-array)

**思路：**

直接统计 `target` 出现的次数，然后判断其是否大于 `len(nums) // 2`。


**代码：**
```python
class Solution:
    def isMajorityElement(self, nums: List[int], target: int) -> bool:
        cnt = collections.Counter(nums)
        return cnt[target] > len(nums) // 2
```


### [1151. 最少交换次数来组合所有的 1](https://leetcode-cn.com/contest/biweekly-contest-6/problems/minimum-swaps-to-group-all-1s-together)

**思路：**

由于数组只有 `0` 和 `1` 组成，那么想要把所有的 `1` 挪到一起（即区间全为 `1`， 其余全为 `0`），则这个全为 `1` 的区间长度必为 `sum(data)`。也就是说，我们可以用一个长度为 `sum(data)` 的滑动窗口，自左向右统计，区间内 `0` 的个数即为把 `1` 全移动到这个区间内的代价。如果暴力统计，则时间复杂度会达到 $O(N^2)$，为了不重复统计，我们可以用前缀和来求区间和，这样时间复杂度就降为了 $O(N)$。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1151-1.gif)


**代码：**
```python
class Solution:
    def minSwaps(self, data: List[int]) -> int:
        n = len(data)
        m = sum(data)
        ans = m
        s = [0]
        for i in data:
            s.append(s[-1] + i)
        for i in range(m, n + 1):
            ans = min(ans, m - (s[i] - s[i - m]))
        return ans
```


### [1152. 用户网站访问行为分析](https://leetcode-cn.com/contest/biweekly-contest-6/problems/analyze-user-website-visit-pattern)

**思路：**

先统计每个用户的访问记录，再将每个用户的访问记录根据时间排序。然后枚举每个用户按照时间顺序访问的三个页面路径，这里可以用一个三重循环，也可以用更通用的深度优先搜索。

统计每个用户访问记录所产生所有的三个页面路径之后，把所有这样的三个路径在一个集合里进行排序，最后枚举进行统计访问次数即可。


**代码：**
```python
class Solution:
    def mostVisitedPattern(self, username: List[str], timestamp: List[int], website: List[str]) -> List[str]:
        d = dict()
        n = len(username)
        for i in range(n):
            if username[i] in d:
                d[username[i]].append((timestamp[i], website[i]))
            else:
                d[username[i]] = [(timestamp[i], website[i])]
        for u in d:
            d[u].sort()
        s = dict()
        for u in d:
            s[u] = set()
        
        def dfs(u, index, dep, n, state):
            if dep >= 3:
                res = []
                for i in range(n):
                    if (state >> i) & 1:
                        res.append(d[u][i][1])
                res = tuple(res)
                s[u].add(res)
                return
            for i in range(index, n - 2 + dep):
                dfs(u, i + 1, dep + 1, n, state | (1 << i))
            return
        
        for u in d:
            dfs(u, 0, 0, len(d[u]), 0)
        
        tot = set()
        for u in s:
            tot |= s[u]

        ans = None
        m = 0
        for t in sorted(tot):
            ts = 0
            for u in s:
                if t in s[u]:
                    ts += 1
            if ts > m:
                m = ts
                ans = t
        return list(ans)
```


### [1153. 字符串转化](https://leetcode-cn.com/contest/biweekly-contest-6/problems/string-transforms-into-another-string)

**思路：**

分类讨论：

1. 当 `str1 == str1` 时，显然是可以转化的。
2. 当 `str1 != str2` 时，我们需要建立从 `str1` 到 `str2` 的映射，此映射必须是多对一或者一对一，不能出现一对多的情况，例如 `str1 = "aa"` 根据规则不能转化为 `str2 = "bc"`，因为无论怎么改变 `'a'`，也不能让两个 `'a'` 变成不相等的 `'b'` 和 `'c'`，所以一旦字典中出现一对多的情况，我们直接返回 `False`。
3. 判断过映射之后，我们最后还需要判断 `str2` 中是否 26 个字母都出现过，因为一旦都出现过，就不会有多余的字母来进行置换了，所有改变都会造成 `str1` 中字符出现联动的情况，达不到转化的目的，例如 `str1 = "abcdefghijklmnopqrstuvwxyz"` `str2 = "bcdefghijklmnopqrstuvwxyza"`。


**代码：**
```python
class Solution:
    def canConvert(self, str1: str, str2: str) -> bool:
        if str1 == str2:
            return True
        n = len(str2)
        d = dict()
        for i in range(n):
            if str1[i] in d:
                if d[str1[i]] != str2[i]:
                    return False
            else:
                d[str1[i]] = str2[i]
        return False if len(set(str2)) == 26 else True
```


