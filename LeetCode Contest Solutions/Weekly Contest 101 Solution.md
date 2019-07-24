## [第 101 场周赛](https://leetcode-cn.com/contest/weekly-contest-101)

本周比赛难度较高，考察了数学、单调栈、分治、动态规划等知识。

### [900. RLE 迭代器](https://leetcode-cn.com/contest/weekly-contest-101/problems/rle-iterator)

**思路：**

直接模拟，因为 `A[i]` 值较大，所以将 `[3,8,0,9,2,5]` 映射成 `[8,8,8,5,5]` 存储的方式不可取，会导致内存溢出。所以应该将 `A` 直接存储，每次调用 `next` 时候，从数组头部开始检查，如果 `A[0]` 小于`n`，则将 `A[0]` 和 `A[1]` 移除队列，并将 `n` 自身减去 `A[0]` ，直到检查到 `A[0]` 大于等于 `n` ，记最后被耗去的项是 `A[1]`，并将 `A[0]` 减去 `n`。

时间复杂度$O(N)$

空间复杂度$O(N)$

**图解：**

![图解](http://qiniu.wenyuetech.cn/900-1.gif)


**代码：**
```python
class RLEIterator:

    def __init__(self, A: List[int]):
        self.RLE = A

    def next(self, n: int) -> int:
        # 返回最后删去的项，默认不存在，为-1
        last = -1
        # 当队列不为空，且第一项计数小于n时
        while self.RLE and self.RLE[0] < n:
            n -= self.RLE[0]
            self.RLE = self.RLE[2:]
        # 不为空就返回最后一个被删去的项
        if self.RLE:
            last = self.RLE[1]
            self.RLE[0] -= n
            # 删完计数为0则丢弃
            while self.RLE[0] == 0:
                self.RLE = self.RLE[2:]
        return last


# Your RLEIterator object will be instantiated and called as such:
# obj = RLEIterator(A)
# param_1 = obj.next(n)
```


### [901. 股票价格跨度](https://leetcode-cn.com/contest/weekly-contest-101/problems/online-stock-span)

**思路：**

动态规划。我们用数组 `stock`  代表每天股票的价格，直接遍历不是最好的方法，在第 `i` 次调用函数 `next` 的时候，我们考虑第 `i-1` 天的股票价格：若第 `i-1` 天股票价格大于第 `i` 天，我们应该返回答案 `1`；若第 `i-1` 天的股票价格小于等于第 `i` 天，那么第 `i-1` 天左边连续小于等于 `i-1` 天的股票价格显然也小于等于第 `i` 天的股票价格，如果我们用 `spanner` 数组表示每次 `next` 函数输出的结果，那么我们只需要从第 `i-1` 天开始，跳过 `spanner[i-1]` 天，再继续检查第 `i-spanner[i-1]` 天的股票价格即可。

这个过程也可以用单调栈实现，这道题的本质是寻找每个数左边第一个比它严格大的数字，故可以采用单调栈的思想，维护一个单调递减的栈，栈中存放数字的下标，每次新加入一个数字时，若栈顶小于等于当前数字，则出栈直到栈空或者栈顶严格大于当前数字，最终栈顶距离新插入数字的下标的距离就是答案，然后将新数字压栈。

代码还可以进一步优化，当第 `i` 次调用 `next` 函数的时候，前 `i-1` 天小于第 `i` 天的股票价格就没必要保存了，我们直接在单调栈中，既保存股票价格又保存股票价格的时间跨度即可。

时间复杂度$O(N)$

空间复杂度$O(N)$

**图解：**

![图解](http://qiniu.wenyuetech.cn/901-1.gif)


**代码：**
```python
class StockSpanner:
    
    def __init__(self):
        self.stock = []
        self.spanner = []
        self.length = 0

    def next(self, price: int) -> int:
        ans = 1
        i = self.length - 1
        while i >= 0 and self.stock[i] <= price:
            ans += self.spanner[i]
            i -= self.spanner[i]
            
        self.length += 1
        self.stock.append(price)
        self.spanner.append(ans)
        
        return ans

# Your StockSpanner object will be instantiated and called as such:
# obj = StockSpanner()
# param_1 = obj.next(price)
```

单调栈实现：

```python
class StockSpanner:

    def __init__(self):
        self.stock = []
        self.stack = []
        self.length = 0

    def next(self, price: int) -> int:
        ans = 0
        while self.stack and self.stock[self.stack[-1]] <= price:
            self.stack.pop()
        
        if not self.stack:
            ans = self.length + 1
        else:
            ans = self.length - self.stack[-1]
        self.stock.append(price)
        self.stack.append(self.length)
        
        self.length += 1
        
        return ans

# Your StockSpanner object will be instantiated and called as such:
# obj = StockSpanner()
# param_1 = obj.next(price)
```

进一步优化：

```python
class StockSpanner(object):

    def __init__(self):
        self.stack = []

    def next(self, price: int) -> int:
        ans = 1
        while self.stack and self.stack[-1][0] <= price:
            ans += self.stack.pop()[1]
        self.stack.append((price, ans))
        return ans

# Your StockSpanner object will be instantiated and called as such:
# obj = StockSpanner()
# param_1 = obj.next(price)
```


### [902. 最大为 N 的数字组合](https://leetcode-cn.com/contest/weekly-contest-101/problems/numbers-at-most-n-given-digit-set)

**思路：**

比`N`低位的直接枚举相加$\sum_{i=1}^{len(N)-1}len(D)^i$，与`N`位数相同的，就从高位到低位依次比较，当前位`D`中有`k`个小于等于`N[i]`：若`k`位全小于，则结束比较；若有一位等于`N[i]`，则递归地继续比较。若`N`中数字全部都在集合`D`中，则答案加`1`。


**代码：**

循环实现

```python
class Solution:
    def atMostNGivenDigitSet(self, D, N):
        """
        :type D: List[str]
        :type N: int
        :rtype: int
        """
        nums_D = [int(i) for i in D]
        nums_N = []
        while N > 0:
            nums_N.insert(0, N % 10)
            N //= 10
        len_D = len(nums_D)
        len_N = len(nums_N)
        ans = 0
        dig = [1] * len_N
        for i in range(1, len(nums_N)):
            dig[i] = len_D * dig[i - 1]
            ans += dig[i]
        all_satisfied = True
        for i in range(len_N):
            for j in nums_D:
                if j < nums_N[i]:
                    ans += dig[len_N-i-1]
            if nums_N[i] not in nums_D:
                all_satisfied = False
                break
        if all_satisfied:
            ans += 1
        return ans
```

递归实现

```python
class Solution:
    def atMostNGivenDigitSet(self, D, N):
        """
        :type D: List[str]
        :type N: int
        :rtype: int
        """
        D = [int(d) for d in D]
        N = self.split(N)
        r = self.count(D,N)
        for i in range(1,len(N)):
            r += len(D)**i
        return r
    def count(self, D, N):
        if len(N) == 0:
            return 0
        if len(N) == 1:
            return len([d for d in D if d <= N[0]])
        r=(len([d for d in D if d < N[0]]))*(len(D) ** (len(N) - 1))
        if N[0] in D:
            r+=self.count(D, N[1:])
        return r
    def split(self, N):
        result = []
        while(N > 0):
            result.append(N % 10)
            N //= 10
        result.reverse()
        return result
```
### [903. DI 序列的有效排列](https://leetcode-cn.com/contest/weekly-contest-101/problems/valid-permutations-for-di-sequence)

**思路：**

1. 分治算法+区间动态规划

   区间动态规划，令 `f(i,j)` 表示 `j−i+1` 个数的排列，满足区间 `S(i,j−1)` 的方案数；

   我们每次枚举最大数字的位置，其中可以放在区间开头，放在区间末尾，或者放在区间中某个位置；

   放在区间开头时，若 `S(i) == 'D'`，则我们转移 `f(i,j) += f(i+1,j)`；

   放在区间末尾时，若 `S(j - 1) == 'I'`，则我们转移 `f(i,j) += f(i,j−1)`；

   否则，枚举位置 `k in [i+1,j−1]`，将区间分为两部分，若`S(k - 1) == 'I'` 并且 `S(k) == 'D'`，则 根据乘法原理和组合数计算，转移 `f(i,j) += C(len−1,k−i) ∗ f(i,k−1) ∗ f(k+1,j)`，其中 `C(len−1,k−i)` 为组合数，这里代表从 `len−1` 个数中选择 `k−i` 个数的方案数。

2. 顺序动态规划+状态压缩

   `dp[i][j]`代表符合`DI`规则的前`i`个位置的由`j`结尾的数组的数目，那么可以求得递推公式：

   `DI`字符串在`i`位置是`'D'`：`dp[i][j] += dp[i-1][k] for k >= j`

   `DI`字符串在`i`位置是`'I'`：`dp[i][j] += dp[i-1][k] for k < j`

   由递推公式可以看出我们需要的是`dp[i][0],dp[i][1],...,dp[i][j]`的和，因此我们改变`dp[i][j]`的意义，`dp[i][j]`此时代表前述的和，做到这一点只需要在代码中添加`dp[i][j]+=dp[i][j-1]`

时间复杂度$O(N^2)$

空间复杂度$O(N^2)$


**代码：**

区间动态规划

```python
class Solution:
    def __init__(self):
        self.memo = {'':1, 'D':1, 'I':1} # 记忆化
    def numPermsDISequence(self, S):
        """
        :type S: str
        :rtype: int
        """
        # 分治 + 动态规划
        # time complexity: O(n^2)
        n = len(S)
        if S in self.memo:
            return self.memo[S]
        CONST = 10**9 + 7
        ans = 0
        if S[0] == "D": # 最大数出现在最左端
            ans += self.numPermsDISequence(S[1:])
        if S[-1] == "I": # 最大数出现在最右端
            ans += self.numPermsDISequence(S[:-1])
        comb = 1 # 组合数
        for i in range(n-1):
            comb = comb*(n-i)//(i+1)
            if S[i:i+2] == "ID": # 最大数出现在中间
                temp1, temp2 = S[:i], S[i+2:]
                ans += self.numPermsDISequence(temp1)*self.numPermsDISequence(temp2)*comb
                ans %= CONST
        self.memo[S] = ans
        return ans
```

顺序动态规划

```python
class Solution:
    def numPermsDISequence(self, S):
        """
        :type S: str
        :rtype: int
        """
        mod = 10 ** 9 + 7
        n = len(S)
        dp = [[0 for _ in range(n+1)] for _ in range(n+1)]
        dp[0][0] = 1
        for i in range(1, n + 1):
            for j in range(i + 1):
                if S[i - 1] == 'D':
                    for k in range(j, i + 1):
                        # here start from j, regard as swap value j with i, then shift all values no larger than j
                        dp[i][j] += dp[i - 1][k]
                        dp[i][j] %= mod
                else:
                    for k in range(0, j):
                        dp[i][j] += dp[i - 1][k]
                        dp[i][j] %= mod
        #print(dp)
        return sum(dp[n]) % mod
```

状态压缩写法

```python
class Solution:
    def numPermsDISequence(self, S):
        """
        :type S: str
        :rtype: int
        """
        dp = [1] * (len(S) + 1)
        for c in S:
            if c == "I":
                dp = dp[:-1]
                for i in range(1, len(dp)):
                    dp[i] += dp[i - 1]
            else:
                dp = dp[1:]
                for i in range(len(dp) - 1)[::-1]:
                    dp[i] += dp[i + 1]
        return dp[0] % (10**9 + 7)
```

一种更简洁的写法

```python
class Solution:
    def numPermsDISequence(self, S):
        """
        :type S: str
        :rtype: int
        """
        r = [1]
        for si in S:
            if si=='D':
                nr = [0]
                for ri in r[::-1]:
                    nr.append((nr[-1]+ri)%1000000007)
                nr = nr[::-1]
            else:
                nr = [0]
                for ri in r:
                    nr.append((nr[-1]+ri)%1000000007)
            r = nr
        return sum(r)%1000000007
```

