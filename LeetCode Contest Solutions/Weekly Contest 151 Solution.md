## [第 151 场周赛](https://leetcode-cn.com/contest/weekly-contest-151)

本周比赛注重考查代码能力，用到字符串处理、数组和链表的遍历、优先队列等算法。

### [1169. 查询无效交易](https://leetcode-cn.com/contest/weekly-contest-151/problems/invalid-transactions)

**思路：**

按照题意遍历每笔交易：第一遍先检查每个交易金额是否超过 `1000`，如果超过则加入答案集合中；第二遍检查每两个交易是否同名不同城，且交易时间相差不超过 `60` 分钟，如果是，则两者都加入答案集合中。最后返回答案集合的列表形式。


**代码：**
```python
class Solution:
    def invalidTransactions(self, transactions: List[str]) -> List[str]:
        d = dict()
        ans = set()
        n = len(transactions)
        sp = []
        for t in transactions:
            s = t.split(',')
            sp.append(s)
            amount = int(s[2])
            if amount > 1000:
                ans.add(t)
        for i in range(n - 1):
            for j in range(i + 1, n):
                if sp[i][0] == sp[j][0] and sp[i][3] != sp[j][3] and abs(int(sp[i][1]) - int(sp[j][1])) <= 60:
                    ans.add(transactions[i])
                    ans.add(transactions[j])
        return list(ans)
                
```
### [1170. 比较字符串最小字母出现频次](https://leetcode-cn.com/contest/weekly-contest-151/problems/compare-strings-by-frequency-of-the-smallest-character)

**思路：**

根据题意实现 `f()` 函数，然后将 `words` 中所有经过函数 `f()` 运算后的结果记入一个数组中。然后遍历 `queries `，将每个字符串经过函数 `f()` 运算后的结果与 `words` 的结果比较，得出答案。


**代码：**
```python
class Solution:
    def numSmallerByFrequency(self, queries: List[str], words: List[str]) -> List[int]:
        def f(s):
            c = collections.Counter(s)
            k = min(c.keys())
            return c[k]
        wc = []
        for w in words:
            wc.append(f(w))
        ans = []
        for q in queries:
            cnt = 0
            qf = f(q)
            for i in wc:
                if i > qf:
                    cnt += 1
            ans.append(cnt)
        return ans
```


### [1171. 从链表中删去总和值为零的连续节点](https://leetcode-cn.com/contest/weekly-contest-151/problems/remove-zero-sum-consecutive-nodes-from-linked-list)

**思路：**

建立一个值为 `0` 的哑结点指向 `head`，然后遍历链表并记录前缀和，遇到相等的前缀和，则说明该段链表和为 `0`， 将其删去，即将上一个前缀和一样结点的 `next` 指针指向本节点的 `next` 结点。最后返回 `ans.next`。

也可以将所有结点值加入到一个数组里进行处理，再重新生成链表。


**代码：**
```python
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def removeZeroSumSublists(self, head: ListNode) -> ListNode:
        ans = ListNode(0)
        ans.next = head
        cur = ans
        d = {0: ans}
        s = 0
        while cur.next:
            cur = cur.next
            s += cur.val
            if s in d:
                d[s].next = cur.next
            else:
                d[s] = cur
        return ans.next
```


### [1172. 餐盘栈](https://leetcode-cn.com/contest/weekly-contest-151/problems/dinner-plate-stacks)

**思路：**

用 `self.cap` 表示每个栈的容量，用 `self.stack` 表示餐盘栈，用 `self.index` 表示没有满的栈的索引。用最小堆维护从左往右第一个没有满的栈。

1. 在 `push` 操作时候：如果所有栈都满，即 `self.index` 为空，则增加一个栈并将元素 `push` 进去，如果 `self.cap == 1`，说明一个元素就装满了，不用做任何操作，如果 `self.cap > 1`，则说明这个栈没有满，将其加入最小堆；如果最小堆 `self.index` 不为空，则说明有没满的栈，取出左边第一个没满的栈，将元素入栈，如果还没满，则将这个栈的索引重新加入最小堆。
2. 在 `pop` 操作的时候，我们将右边的空栈都移出，找到右边第一个不为空的栈，将其栈顶元素弹出，如果本来栈是满的，且 `self.cap > 1`，那么弹出后栈不满，则需要将索引加入最小堆。
3. 在 `popAtStack` 操作的时候，检查索引是否在 `len(self.stack)` 之内，如果没有，则返回 `-1`，如果索引合法，则检查对应栈是否为空，如果为空，返回 `-1`，如果不为空，则弹出元素，如果栈由满变为未满，则将索引加入最小堆。


**代码：**
```python
class DinnerPlates:

    def __init__(self, capacity: int):
        self.cap = capacity
        self.stack = []
        self.index = []

    def push(self, val: int) -> None:
        if not self.index:
            self.stack.append([])
            self.stack[-1].append(val)
            if self.cap > 1:
                self.index = [len(self.stack) - 1]
        else:
            index = heapq.heappop(self.index)
            self.stack[index].append(val)
            if len(self.stack[index]) < self.cap:
                heapq.heappush(self.index, index)

    def pop(self) -> int:
        while self.stack and not self.stack[-1]:
            self.stack.pop()
        if self.stack:
            if len(self.stack[-1]) == self.cap and self.cap > 1:
                heapq.heappush(self.index, len(self.stack) - 1)
            return self.stack[-1].pop()
        else:
            return -1

    def popAtStack(self, index: int) -> int:
        if index < len(self.stack):
            if self.stack[index]:
                if len(self.stack[index]) == self.cap and self.cap > 1:
                    heapq.heappush(self.index, index)
                return self.stack[index].pop()
            else:
                return -1
        else:
            return -1


# Your DinnerPlates object will be instantiated and called as such:
# obj = DinnerPlates(capacity)
# obj.push(val)
# param_2 = obj.pop()
# param_3 = obj.popAtStack(index)
```


