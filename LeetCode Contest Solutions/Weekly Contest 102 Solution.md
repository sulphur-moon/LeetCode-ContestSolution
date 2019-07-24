## [第 102 场周赛](https://leetcode-cn.com/contest/weekly-contest-102)

本周比赛算法方面不难，考察了数学、单调栈、双指针等知识。考察对题目的理解和思维能力。

### [905. 按奇偶排序数组](https://leetcode-cn.com/contest/weekly-contest-102/problems/sort-array-by-parity)

**思路：**

没有空间复杂度要求的话，可以开两个数组，一个存储偶数，另一个存储奇数，然后一边遍历原数组一边统计，遍历后把偶数数组和奇数数组连接起来输出即可。

如果要求不另开数组，在原数组上操作的话，那么需要用双指针遍历。双指针遍历有两种方法：一种是双指针同向遍历，初始状态都指在数组左端，后面指针不断加一，遇到偶数就交换到前面去，再把前面指针加一，指导后面指针遍历完数组结束；另外一种是双指针相向遍历，初始状态是第一个指针指在数组左端，第二个指针指在数组右端，当两个指针没有相遇时，右边指针向左寻找偶数，左边指针向右寻找奇数，然后交换指针所指的两个元素，直到两个指针相遇为止。

时间复杂度 $O(N)$

空间复杂度 $O(1)$

**图解：**

![图解](http://qiniu.wenyuetech.cn/905-1.gif)


**代码：**

有辅助数组的算法

```python
class Solution:
    def sortArrayByParity(self, A):
        """
        :type A: List[int]
        :rtype: List[int]
        """
        ans1 = []
        ans2 = []
        for i in A:
            if i % 2 == 0:
                ans1.append(i)
            else:
                ans2.append(i)
        return ans1 + ans2
```

双指针同向遍历

```python
class Solution:
    def sortArrayByParity(self, A):
        """
        :type A: List[int]
        :rtype: List[int]
        """
        i = 0
        for j in range(len(A)):
            if A[j] % 2 == 0:
                A[i], A[j] = A[j], A[i]
                i += 1
        return A
```

双指针相向遍历

```python
class Solution(object):
    def sortArrayByParity(self, A):
        """
        :type A: List[int]
        :rtype: List[int]
        """
        
        l = len(A) 
        i, j = 0, l-1
        while i < j:
            while A[i] % 2 == 0 and i < j:
                i += 1
            while A[j] % 2 == 1 and i < j:
                j -= 1
            A[i], A[j] = A[j], A[i]
                    
        return A
```

### [904. 水果成篮](https://leetcode-cn.com/contest/weekly-contest-102/problems/fruit-into-baskets)

**思路：**

顺序遍历或者倒序遍历都可以。以从后往前的倒序遍历为例，用 `fruit` 数组表示两个水果种类代号，将 `tree[len(tree)-1]` 加入到 `fruit` 中，然后指针从最后一棵树开始，往前遍历寻找另一种不同水果。如果找不到，说明只有一种水果，直接返回 `len(tree)`。如果找到了，将第二种水果加入到 `fruit` 中，用 `start` 和 `stop` 数组表示两个水果在区间的起始位置和结束位置，则每扫描一个区间，最大长度为 `max(stop)-min(start)`，继续扫描下个区间，这时要判断篮子里保存哪个水果，所以需要比较两个水果的起始位置，保留 `start` 值较小的那种类型的水果，将另一种水果用当前指针新发现的水果替换，保留水果的 `stop` 值还要用被替换水果的 `start` 值更新，即 `stop[0] = min(stop[0], start[1] - 1)`。

时间复杂度 $O(N)$

空间复杂度 $O(1)$

**图解：**

![图解](http://qiniu.wenyuetech.cn/904-1.gif)


**代码：**

倒序遍历

```python
class Solution:
    def totalFruit(self, tree):
        """
        :type tree: List[int]
        :rtype: int
        """
        l_tree = len(tree)

        if l_tree <= 2:
            return l_tree

        ans = 2

        l = l_tree - 1
        fruit = [tree[l], tree[l]]
        start = [l, l]
        stop = [l, l]

        # find the other fruit
        i = l
        while i >= 0 and tree[i] == fruit[0]:
            i -= 1
        # only one kind of fruit
        if i < 0:
            return l_tree
        else:
            fruit[1] = tree[i]
            start[0] = i + 1
            start[1] = i
            stop[1] = i

        i -= 1
        while i >= 0:
            while i >= 0:
                if tree[i] == fruit[0]:
                    start[0] = i
                elif tree[i] == fruit[1]:
                    start[1] = i
                else:
                    break
                i -= 1

            ans = max(ans, stop[0] - i)
            if start[0] > start[1]:
                fruit = fruit[::-1]
                start = start[::-1]
                stop = stop[::-1]

            stop[0] = min(stop[0], start[1] - 1)
            fruit[1] = tree[i]
            start[1] = i
            stop[1] = i
        
        ans = max(ans, stop[0] - i)
        return ans
```

顺序遍历

```python
class Solution:
    def totalFruit(self, tree):
        """
        :type tree: List[int]
        :rtype: int
        """
        ans = 0
        to_end = 1
        start = 0
        found = {tree[0]}
        for i in range(1, len(tree)):
            if tree[i] in found:
                to_end += 1
            elif len(found) < 2:
                found.add(tree[i])
                to_end += 1
            else:
                ans = max(to_end, ans)
                to_end = i - start + 1
                found = {tree[i], tree[i-1]}
            # 这里更新两种水果的分界点
            if tree[i] != tree[i-1]:
                start = i
        return max(to_end, ans)
```

### [907. 子数组的最小值之和](https://leetcode-cn.com/contest/weekly-contest-102/problems/sum-of-subarray-minimums)

**思路：**

考虑从 `A` 中的每个元素 `A[i]`，如果求出包含 `A[i]` 并以 `A[i]` 为最小元素的所有子数组个数 `n[i]`，则元素 `A[i]` 对答案 `ans` 的贡献为 `n[i] * A[i]`，那么我们可以先求包含 `A[i]` 并以 `A[i]` 为最小元素的最长子数组，如果 `A[i]` 左边第一个小于 `A[i]` 的元素为 `A[left]`，`A[i]` 右边第一个小于 `A[i]` 的元素为 `A[right]`，则包含 `A[i]` 并以 `A[i]` 为最小元素的最长子数组为 `A[left+1:right]`，满足以 `A[i]` 为最小元素的所有子数组个数 `n[i] = (i-left)*(right-i)`。我们用 `left[i]` 表示 `A[i]` 左边第一个小于 `A[i]` 元素的位置，用 `right[i]` 表示 `A[i]` 右边第一个小于 `A[i]` 元素的位置，`left` 数组初始值为 `-1`，`right` 数组初始值为 `len(A)`，求解 `left` 和 `right` 可以用单调栈来实现，可以两遍遍历，也可以一遍遍历，更优化的写法还可以一边遍历一边求解 `ans`。

时间复杂度 $O(N)$

空间复杂度 $O(N)$

**图解：**

![图解](http://qiniu.wenyuetech.cn/907-1.gif)


**代码：**

```python
class Solution:
    def sumSubarrayMins(self, A):
        """
        :type A: List[int]
        :rtype: int
        """
        len_A = len(A)
        if len_A == 0:
            return 0
        if len_A == 1:
            return A[0]
        
        ans = 0
        left = [0] * len_A
        right = [0] * len_A
        
        stack = []
        for i in range(len_A):
            while stack and A[stack[-1]] > A[i]:
                stack.pop()
            if not stack:
                left[i] = -1
            else:
                left[i] = stack[-1]
            stack.append(i)
        
        stack = []
        for i in range(len_A - 1, -1, -1):
            while stack and A[stack[-1]] >= A[i]:
                stack.pop()
            if not stack:
                right[i] = len_A
            else:
                right[i] = stack[-1]
            stack.append(i)
        
        for i in range(len_A):
            ans += (i - left[i]) * (right[i] - i) * A[i]
            ans %= 1000000007
        return ans
```

一遍遍历

```python
class Solution:
    def sumSubarrayMins(self, A):
        """
        :type A: List[int]
        :rtype: int
        """
        ans = 0
        A = [float('-inf')] + A + [float('-inf')]
        stack = []
        for i, a in enumerate(A):
            while stack and A[stack[-1]] > a:
                cur = stack.pop()
                ans += A[cur] * (i-cur) * (cur-stack[-1])
            stack.append(i)
        return ans % (10**9 + 7)
```

### [906. 超级回文数](https://leetcode-cn.com/contest/weekly-contest-102/problems/super-palindromes)

**思路：**

从1产生回文数，把产生的回文数平方，判断平方后是不是回文数并在`[L, R]`内。

由于超级回文数的个数十分有限，所以也可以打表解决。

时间复杂度 $O(\sqrt{N})$

空间复杂度 $O(1)$


**代码：**

```python
class Solution:
    def superpalindromesInRange(self, L, R):
        """
        :type L: str
        :type R: str
        :rtype: int
        """
        def is_circle(num):
            s = str(num)
            return s == s[::-1]

        def create_circle(num):
            s = str(num)
            first = int(s + s[::-1])
            second = int(s[:-1] + s[::-1])
            return first, second

        l = int(math.sqrt(int(L)))
        r = int(math.sqrt(int(R))) + 1
        # print(l, r)
        ans = 0
        for num in range(1, 100000):
            # print(num)
            big, small = create_circle(num)
            # print(big, small)
            if l <= small < r:
                if is_circle(small * small):
                    ans += 1
            if l <= big < r:
                if is_circle(big * big):
                    ans += 1
            if small > r:
                break
        return ans
```


