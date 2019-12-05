## [第 108 场周赛](https://leetcode-cn.com/contest/weekly-contest-108)

本周比赛不难，但是比较有技巧性，用到字符串处理，动态规划、分治等算法。

### [929. 独特的电子邮件地址](https://leetcode-cn.com/contest/weekly-contest-108/problems/unique-email-addresses)

**思路：**

先用 `'@'` 分割字符，前半部分用 `'+'` 分割后只保留第一部分，并将其中的 `'.'` 去除，求得 `local`，然后将 `local` 和 `domain` 用 `'@'` 重新连接加入集合，最终集合的长度就是答案。

时间复杂度 $O(N)$

空间复杂度 $O(N)$


**代码：**
```python
class Solution:
    def numUniqueEmails(self, emails: List[str]) -> int:
        ans = set()
        for email in emails:
            temp = email.split("@")
            local = temp[0].split('+')[0]
            local = local.replace('.', '')
            domain = temp[1]
            ans.add('@'.join([local, domain]))
        return len(ans)
```


### [930. 和相同的二元子数组](https://leetcode-cn.com/contest/weekly-contest-108/problems/binary-subarrays-with-sum)

**思路：**

一次遍历，从前往后枚举区间终点，同时用一个数组记录当前不同前缀和的数量，用 `f[i]` 代表和为 `i` 的前缀和个数。假设枚举的当前坐标是 `j`，那么我们的目标就是计算`j`之前共有多少个前缀和是 `sum[j] - S`，这个值就是 `f[sum[j] - S]`。由于遍历过程中，每个前缀和 `sum[j]` 只用了一次，所以我们可以用一个变量 `s` 来表示，减少空间复杂度。

时间复杂度 $O(N)$

空间复杂度 $O(N)$


**代码：**
```python
class Solution:
    def numSubarraysWithSum(self, A: List[int], S: int) -> int:
        s = 0
        f = [0] * (len(A) + 1)
        f[0] = 1
        ans = 0
        for i in A:
            s += i
            if s >= S:
                ans += f[s - S]
            f[s] += 1
        return ans
```


### [931. 下降路径最小和](https://leetcode-cn.com/contest/weekly-contest-108/problems/minimum-falling-path-sum)

**思路：**

动态规划入门题，和 POJ1163 基本相同，自底向上动态规划，（其实自顶向下也一样），状态转移方程为：`A[row][col] += min(A[row + 1][col - 1], A[row + 1][col], A[row + 1][col + 1])`。

时间复杂度 $O(N^2)$

空间复杂度 $O(1)$


**代码：**
```python
class Solution:
    def minFallingPathSum(self, A: List[List[int]]) -> int:
        l = len(A)
        if l == 1:
            return A[0][0]
        for row in range(l - 2, -1, -1):
            A[row][0] += min(A[row + 1][0], A[row + 1][1])
            A[row][-1] += min(A[row + 1][-1], A[row + 1][-2])
            for col in range(1, l - 1):
                A[row][col] += min(A[row + 1][col - 1], A[row + 1][col], A[row + 1][col + 1])
        return min(A[0])
```


### [932. 漂亮数组](https://leetcode-cn.com/contest/weekly-contest-108/problems/beautiful-array)

**思路：**

分治法：

1. 对于一个连续的数列 `1,2,3,…,n`，如果按照奇偶分成两部分，`1,3,5,…` 放到左边，`2,4,6,8,… ` 放到右边。这样重新安排后，如果 `i` 属于左边，`j` 属于右边，`A[i]+A[j]` 就必定是奇数，因而不存在 `A[k]`，满足 `A[k]∗2=A[i]+A[j]`。
2. 接下来再看每一部分的内部，由于 `1,3,5,… ` 也是等差数列，所以可以经过变换再次变成 `1,2,3,…`，且变换后的数列如果满足题目的性质，则原数列同样满足。如果我们仍然按照 1 中的策略进行奇偶分离，则可以继续分为两部分递归处理。同理 `2,4,6,…` 也可以进行变换然后递归。
3. 最后递归的出口是仅有一个数字时，直接返回。

时间复杂度 $O(NlogN)$

空间复杂度 $O(N)$


**代码：**
```python
class Solution:
    def beautifulArray(self, N: int) -> List[int]:
        if N == 1:
            return [1]
        if N == 2:
            return [1, 2]
        ans = [i for i in range(1, N + 1)]
        
        def change(A):
            if len(A) <= 1:
                return A
            A1 = []
            A2 = []
            for i in range(len(A)):
                if i % 2 == 0:
                    A1.append(A[i])
                else:
                    A2.append(A[i])
            return change(A1) + change(A2)
        
        return change(ans)
```

 更简单的写法：

```python
class Solution:
    def beautifulArray(self, N: int) -> List[int]:
        def helper(nums):
            return helper(nums[::2]) + helper(nums[1::2]) if len(nums) > 2 else nums
        return helper(list(range(1,N + 1)))
```


