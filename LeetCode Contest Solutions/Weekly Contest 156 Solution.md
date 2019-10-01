## [第 156 场周赛](https://leetcode-cn.com/contest/weekly-contest-156)

本周比赛考察了数学统计、栈、滑动窗口、广度优先搜索、动态规划等算法。

### [1207. 独一无二的出现次数](https://leetcode-cn.com/contest/weekly-contest-156/problems/unique-number-of-occurrences)

**思路：**

统计每个数字出现的频次，然后比较 `keys()` 的长度和 `set(values())` 的长度即可达到去重比较的目的。


**代码：**
```python
class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        cnt = collections.Counter(arr)
        return len(cnt) == len(set(cnt.values()))
```


### [1208. 删除字符串中的所有相邻重复项 II](https://leetcode-cn.com/contest/weekly-contest-156/problems/remove-all-adjacent-duplicates-in-string-ii)

**思路：**

将元素依次入栈并统计元素数量。每次入栈判断是否和栈顶元素相同：如果与栈顶元素相同，那么将栈顶元素的数量加 1；如果栈顶元素数量达到 3，则将栈顶元素出栈；如果待入栈元素与栈顶元素不同，那么直接入栈并将该元素个数置为 1。遍历完字符串之后，将栈中剩余元素拼接即为答案。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1208-1.gif)


**代码：**
```python
class Solution:
    def removeDuplicates(self, s: str, k: int) -> str:
        n = len(s)
        stack = []
        for c in s:
            if not stack or stack[-1][0] != c:
                stack.append([c, 1])
            elif stack[-1][1] + 1 < k:
                stack[-1][1] += 1
            else:
                stack.pop()
        ans = ""
        for c, l in stack:
            ans += c * l
        return ans
```


### [1209. 尽可能使字符串相等](https://leetcode-cn.com/contest/weekly-contest-156/problems/get-equal-substrings-within-budget)

**思路：**

滑动窗口法。先对每个位置 `i` 求出替换的花费，用 `costs[i]` 表示。然后从左向右开始逐步增加窗口宽度，累加 `costs[i]`，并不断更新答案。当 `costs[i]` 累加值 `c ` 超过 `maxCost` 时，将窗口左端 `start` 右移，直到再次满足累加值 `c` 小于等于 `maxCost`，更新答案，并继续扩展窗口右端。如此往复，直到右端点遍历完整个 `costs` 数组。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1209-1.gif)


**代码：**
```python
class Solution:
    def equalSubstring(self, s: str, t: str, maxCost: int) -> int:
        n = len(s)
        costs = [0] * n
        for i in range(n):
            costs[i] = abs(ord(s[i]) - ord(t[i]))
        start, c, ans = -1, 0, 0
        for i in range(n):
            c += costs[i]
            while start < i and c > maxCost:
                start += 1
                c -= costs[start]
            ans = max(ans, i - start)
        return ans
```


### [1210. 穿过迷宫的最少移动次数](https://leetcode-cn.com/contest/weekly-contest-156/problems/minimum-moves-to-reach-target-with-rotations)

**思路：**

本题虽然难度为 `hard`，但是算法层面并不难，只是需要理解题目意思和代码设计能力。算法可以采用广度优先搜索，也可以用动态规划，把题目描述的所有种类的移动实现即可。


**代码：**
```python
from collections import deque

class Solution:
    def minimumMoves(self, grid: List[List[int]]) -> int:
        n = len(grid)
        queue = deque()
        queue.append((0, 0, 0, 1))
        visited = set()
        visited.add((0, 0, 0, 1))
        ans = 0
        while queue:
            l = len(queue)
            for _ in range(l):
                tailx, taily, headx, heady = queue.popleft()
                if tailx == n-1 and taily == n-2 and headx == n-1 and heady == n-1:
                    return ans
                if taily+1 < n and grid[tailx][taily+1] == 0 and heady+1 < n and grid[headx][heady+1] == 0 and (tailx, taily+1, headx, heady+1) not in visited:
                    queue.append((tailx, taily+1, headx, heady+1))
                    visited.add((tailx, taily+1, headx, heady+1))
                if tailx+1 < n and grid[tailx+1][taily] == 0 and headx+1 < n and grid[headx+1][heady] == 0 and (tailx+1, taily, headx+1, heady) not in visited:
                    queue.append((tailx+1, taily, headx+1, heady))
                    visited.add((tailx+1, taily, headx+1, heady))
                if tailx == headx:
                    if tailx+1 < n and grid[tailx+1][taily] == 0 and grid[headx+1][heady] == 0 and (tailx, taily, headx+1, heady-1) not in visited:
                        queue.append((tailx, taily, headx+1, heady-1))
                        visited.add((tailx, taily, headx+1, heady-1))
                else:
                    if taily+1 < n and grid[tailx][taily+1] == 0 and grid[headx][heady+1] == 0 and (tailx, taily, headx-1, heady+1) not in visited:
                        queue.append((tailx, taily, headx-1, heady+1))
                        visited.add((tailx, taily, headx-1, heady+1))
            ans += 1
        return -1
```


