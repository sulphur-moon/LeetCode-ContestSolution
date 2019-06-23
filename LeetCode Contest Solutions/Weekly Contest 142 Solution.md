## Weekly Contest 142 Solution

本周比赛算法方面不难，用到的都是较为基础的遍历、排序、二分查找、深度优先搜索（栈、递归）等算法。但是对于题目意思的理解和代码编写能力要求较高。

### [1093. 大样本统计](https://leetcode-cn.com/contest/weekly-contest-142/problems/statistics-from-a-large-sample/)

我们对 `0` 到 `255` 之间的整数进行采样，并将结果存储在数组 `count` 中：`count[k]` 就是整数 `k` 的采样个数。

我们以 **浮点数** 数组的形式，分别返回样本的最小值、最大值、平均值、中位数和众数。其中，众数是保证唯一的。

我们先来回顾一下中位数的知识：

- 如果样本中的元素有序，并且元素数量为奇数时，中位数为最中间的那个元素；
- 如果样本中的元素有序，并且元素数量为偶数时，中位数为中间的两个元素的平均值。

**示例 1：**

```
输入：count = [0,1,3,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
输出：[1.00000,3.00000,2.37500,2.50000,3.00000]
```

**示例 2：**

```
输入：count = [0,4,3,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
输出：[1.00000,4.00000,2.18182,2.00000,1.00000]
```

**提示：**

1. `count.length == 256`
2. `1 <= sum(count) <= 10^9`
3. 计数表示的众数是唯一的
4. 答案与真实值误差在 `10^-5` 以内就会被视为正确答案

**思路：**

由题意，我们知道`count`为固定长度为`256`的整数数组，`count[i]`表示整数`i`在样本中出现的次数，要求返回样本的最大值、最小值、平均值、中位数和众数。

- 最大值就是从数组右边往左数第一个不为`0`的数对应的索引；
- 最小值就是从数组左边往右数第一个不为`0`的数对应的索引；
- 平均值就是把所有的索引（数的值）乘以元素值（出现的频次）再求和，得到样本总和，再除以总频次；
- 中位数的计算，从左到右遍历数组，累加每个值出现的频次：
  - 如果频次总和`n`为奇数，中位数等于频次累加第一次大于等于`n//2+1`的索引；
  - 如果频次总和`n`为偶数，中间两个数，一个是频次累加第一次大于等于`n//2`的索引，另一个是频次累加第一次大于等于`n//2+1`的索引；
- 众数就是数组中元素最大值对应的索引。

时间复杂度 $O(1)$

空间复杂度 $O(1)$

**代码：**

```python
class Solution:
    def sampleStats(self, count: List[int]) -> List[float]:
        n = sum(count)
        left_cnt, right_cnt = 0, 0
        if n % 2 == 0:
            left_cnt, right_cnt = n//2, n//2 + 1
        else:
            left_cnt, right_cnt = n//2 + 1, n//2 + 1
        s, c = 0, 0
        max_cnt, max_cnt_index = 0, 0
        max_cnt_index = 0
        max_num, medium, min_num = 0, 0, -1
        left_flg, right_flg = False, False
        for i in range(256):
            c += count[i]
            if c >= left_cnt and not left_flg:
                medium += i
                left_flg = True
            if c >= right_cnt and not right_flg:
                medium += i
                right_flg = True
            s += count[i] * i
            if count[i] > max_cnt:
                max_cnt = count[i]
                max_cnt_index = i
            if count[i] > 0:
                max_num = i
                if min_num == -1:
                    min_num = i
        return [float(min_num), float(max_num), float(s/n), float(medium/2), float(max_cnt_index)]
```

### [1094. 拼车](https://leetcode-cn.com/contest/weekly-contest-142/problems/car-pooling/)

假设你是一位顺风车司机，车上最初有 `capacity` 个空座位可以用来载客。由于道路的限制，车 **只能** 向一个方向行驶（也就是说，**不允许掉头或改变方向**，你可以将其想象为一个向量）。

这儿有一份行程计划表 `trips[][]`，其中 `trips[i] = [num_passengers, start_location, end_location]` 包含了你的第 `i` 次行程信息：

- 必须接送的乘客数量；
- 乘客的上车地点；
- 以及乘客的下车地点。

这些给出的地点位置是从你的 **初始** 出发位置向前行驶到这些地点所需的距离（它们一定在你的行驶方向上）。

请你根据给出的行程计划表和车子的座位数，来判断你的车是否可以顺利完成接送所用乘客的任务（当且仅当你可以在所有给定的行程中接送所有乘客时，返回 `true`，否则请返回 `false`）。

**示例 1：**

```
输入：trips = [[2,1,5],[3,3,7]], capacity = 4
输出：false
```

**示例 2：**

```
输入：trips = [[2,1,5],[3,3,7]], capacity = 5
输出：true
```

**示例 3：**

```
输入：trips = [[2,1,5],[3,5,7]], capacity = 3
输出：true
```

**示例 4：**

```
输入：trips = [[3,2,7],[3,7,9],[8,3,9]], capacity = 11
输出：true
```

**提示：**

1. 你可以假设乘客会自觉遵守 “**先下后上**” 的良好素质
2. `trips.length <= 1000`
3. `trips[i].length == 3`
4. `1 <= trips[i][0] <= 100`
5. `0 <= trips[i][1] < trips[i][2] <= 1000`
6. `1 <= capacity <= 100000`

**思路：**

按照时间（路程）顺序模拟，把所有的上车点和下车点加入一个列表里，然后从小到大排序，如果有上车点和下车点在一起的话，根据先下后上原则，要把下车点排在前面。然后从头开始遍历列表，模拟经过每个站点车上的人数，如果某个站点车上的人数大于车的容量，那么返回`False`，如果所有站点人数都小于等于车的容量，那么返回`True`。

**代码：**

```python
class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        process = []
        for t in trips:
            process.append((t[1], 1, t[0]))
            process.append((t[2], 0, t[0]))
        process.sort()
        print(process)
        num = 0
        for p in process:
            if p[1] == 1:
                num += p[2]
                if num > capacity:
                    return False
            else:
                num -= p[2]
        return True`
```

### [1095. 山脉数组中查找目标值](https://leetcode-cn.com/contest/weekly-contest-142/problems/find-in-mountain-array/)

（这是一个 **交互式问题** ）

给你一个 **山脉数组** `mountainArr`，请你返回能够使得 `mountainArr.get(index)` **等于** `target` **最小** 的下标 `index` 值。

如果不存在这样的下标 `index`，就请返回 `-1`。

所谓山脉数组，即数组 `A` 假如是一个山脉数组的话，需要满足如下条件：

**首先**，`A.length >= 3`

**其次**，在 `0 < i < A.length - 1` 条件下，存在 `i` 使得：

- `A[0] < A[1] < ... A[i-1] < A[i]`
- `A[i] > A[i+1] > ... > A[A.length - 1]`

你将 **不能直接访问该山脉数组**，必须通过 `MountainArray` 接口来获取数据：

- `MountainArray.get(k)` - 会返回数组中索引为`k` 的元素（下标从 0 开始）
- `MountainArray.length()` - 会返回该数组的长度

**注意：**

对 `MountainArray.get` 发起超过 `100` 次调用的提交将被视为错误答案。此外，任何试图规避判题系统的解决方案都将会导致比赛资格被取消。

为了帮助大家更好地理解交互式问题，我们准备了一个样例 “**答案**”：https://leetcode-cn.com/playground/RKhe3ave，请注意这 **不是一个正确答案**。

**示例 1：**

```
输入：array = [1,2,3,4,5,3,1], target = 3
输出：2
解释：3 在数组中出现了两次，下标分别为 2 和 5，我们返回最小的下标 2。
```

**示例 2：**

```
输入：array = [0,1,2,4,2,1], target = 3
输出：-1
解释：3 在数组中没有出现，返回 -1。
```

**提示：**

1. `3 <= mountain_arr.length() <= 10000`
2. `0 <= target <= 10^9`
3. `0 <= mountain_arr.get(index) <= 10^9`

**思路：**

由于不能调用 `MountainArray.get` 超过`100`次，而`mountain_arr.length()`最大为`10000`，所以要用二分查找来搜索我们要找的目标。给定的`mountainArr`是一个山脉数组，即数组元素按顺序，先单调递增，再单调递减。由于二分查找只作用于有序数列，所以我们先要找到山脉数组的峰顶：如果峰顶小于`target`，直接返回`-1`；如果峰顶等于`target`，直接返回峰顶的索引；如果峰顶大于`target`，那么以峰顶为界，先在上坡中二分查找目标，如果找不到，就在下坡中二分查找目标，都找不到就返回`-1`。

**代码：**

```python
# """
# This is MountainArray's API interface.
# You should not implement it, or speculate about its implementation
# """
#class MountainArray:
#    def get(self, index: int) -> int:
#    def length(self) -> int:

class Solution:
    def findInMountainArray(self, target: int, mountain_arr: 'MountainArray') -> int:
        n = mountain_arr.length()
        self.memo = dict()
        # 获取索引处的元素值
        def getByIndex(index):
            if index not in self.memo:
                self.memo[index] = mountain_arr.get(index)
            return self.memo[index]
        # 查找峰值
        def findPeak(left, right):
            mid = (left + right) // 2
            mid_left = getByIndex(mid - 1)
            mid_num = getByIndex(mid)
            mid_right = getByIndex(mid + 1)
            if mid_left < mid_num and mid_num > mid_right:
                return mid
            if mid_left > mid_num > mid_right:
                return findPeak(left, mid)
            if mid_left < mid_num < mid_right:
                return findPeak(mid, right)
        # 上坡查找元素
        def findNum1(left, right):
            mid = (left + right) // 2
            mid_num = getByIndex(mid)
            if mid_num == target:
                return mid
            if mid_num > target:
                return findNum1(left, mid)
            if mid_num < target:
                if getByIndex(mid + 1) > target:
                    return -1
                return findNum1(mid, right)
        # 下坡查找元素
        def findNum2(left, right):
            mid = (left + right) // 2
            mid_num = getByIndex(mid)
            if mid_num == target:
                return mid
            if mid_num < target:
                if getByIndex(mid - 1) > target:
                    return -1
                return findNum2(left, mid)
            if mid_num > target:
                return findNum2(mid, right)
        # 和最小元素比较
        min_num1 = getByIndex(0)
        min_num2 = getByIndex(n - 1)
        min_num = min(min_num1, min_num2)
        if target < min_num:
            return -1
        # 和峰值比较
        peak = findPeak(0, n - 1)
        max_num = getByIndex(peak)
        if target == max_num:
            return peak
        if target > max_num:
            return -1
        # 上坡查找
        if target == min_num1:
            return 0
        if target > min_num1:
            res = findNum1(0, peak)
            if res != -1:
                return res
        # 下坡查找
        if target == min_num2:
            return n - 1
        if target > min_num2:
            res = findNum2(peak, n)
            if res != -1:
                return res
        return -1
```

### [1096. 花括号展开 II](https://leetcode-cn.com/contest/weekly-contest-142/problems/brace-expansion-ii/)

如果你熟悉 Shell 编程，那么一定了解过花括号展开，它可以用来生成任意字符串。

花括号展开的表达式可以看作一个由 **花括号**、**逗号** 和 **小写英文字母** 组成的字符串，定义下面几条语法规则：

- 如果只给出单一的元素 `x`，那么表达式表示的字符串就只有 `"x"`。 

  - 例如，表达式 `{a}` 表示字符串 `"a"`。
  - 而表达式 `{ab}` 就表示字符串 `"ab"`。

- 当两个或多个表达式并列，以逗号分隔时，我们取这些表达式中元素的并集。

  - 例如，表达式 `{a,b,c}` 表示字符串 `"a","b","c"`。
  - 而表达式 `{a,b},{b,c}` 也可以表示字符串 `"a","b","c"`。

- 要是两个或多个表达式相接，中间没有隔开时，我们从这些表达式中各取一个元素依次连接形成字符串。

  - 例如，表达式 `{a,b}{c,d}` 表示字符串 `"ac","ad","bc","bd"`。

- 表达式之间允许嵌套，单一元素与表达式的连接也是允许的。

  - 例如，表达式 `a{b,c,d}` 表示字符串 `"ab","ac","ad"`。
  - 例如，表达式 `{a{b,c}}{{d,e}f{g,h}}` 可以代换为 `{ab,ac}{dfg,dfh,efg,efh}`，表示字符串 `"abdfg", "abdfh", "abefg", "abefh", "acdfg", "acdfh", "acefg", "acefh`"。

给出表示基于给定语法规则的表达式 `expression`，返回它所表示的所有字符串组成的有序列表。

假如你希望以「集合」的概念了解此题，也可以通过点击 “**显示英文描述**” 获取详情。

**示例 1：**

```
输入："{a,b}{c{d,e}}"
输出：["acd","ace","bcd","bce"]
```

**示例 2：**

```
输入："{{a,z}, a{b,c}, {ab,z}}"
输出：["a","ab","ac","z"]
解释：输出中 不应 出现重复的组合结果。
```

**提示：**

1. `1 <= expression.length <= 50`
2. `expression[i]` 由 `'{'`，`'}'`，`','` 或小写英文字母组成
3. 给出的表达式 `expression` 用以表示一组基于题目描述中语法构造的字符串

**思路：**

将花括号按层展开，用变量`level`表示当前是第几层括号，初始值为`0`，遇到一个左括号`{`时，`level`值增加`1`，遇到右括号`}`时，`level`值减少`1`。用递归处理每一层，每一层的结构为`{}{}...{} + {}{}...{} + ...`，和四则运算法则同理，先调用下一层函数计算括号内的，然后先乘后加。当前层递归函数只用笛卡尔积和并集处理层数为`0`的表达式，进入下一层，就用`start`变量标记该层的起始位置，直到找到该层的结束位置时，调用下一层递归函数。遍历时候，每遇到一个逗号（`,`）就在`groups`里面新开一个`list`，遍历完后，将`groups`里的每个`list`进行笛卡尔积运算，再取并集。

**代码：**

```python
class Solution:
    def braceExpansionII(self, expression: str) -> List[str]:
        groups = [[]]
        level = 0
        for i, c in enumerate(expression):
            if c == '{':
                if level == 0:
                    start = i+1
                level += 1
            elif c == '}':
                level -= 1
                if level == 0:
                    groups[-1].append(self.braceExpansionII(expression[start:i]))
            elif c == ',' and level == 0:
                groups.append([])
            elif level == 0:
                groups[-1].append([c])
                print(c, groups)
        word_set = set()
        # 加运算，取并集
        for group in groups:
            word_set |= set(map(''.join, itertools.product(*group))) # 乘运算，取笛卡尔积
        return sorted(word_set)
```

