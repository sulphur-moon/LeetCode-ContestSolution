## [第 103 场周赛](https://leetcode-cn.com/contest/weekly-contest-103)

本周比赛难度适中，在数学方面需要些技巧，用到的算法有 BFS 和二分查找等。

### [908. 最小差值 I](https://leetcode-cn.com/contest/weekly-contest-103/problems/smallest-range-i)

**思路：**

求数组中的最小值与最大值：如果他们之间的差小于等于 `2*K`，那么数组中的所有数都可以通过加上一个在 `[-K, K]` 之间的数来达到 `(min(A) + max(A)) // 2`；如果他们之间的差大于 `2 * K`，那么处理后的数组差值最小只能达到 `max(A) - min(A) - 2 * K`。


**代码：**
```python
class Solution:
    def smallestRangeI(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: int
        """
        a = max(A)
        b = min(A)
        if (a-b>2*K):
            return a-b-2*K
        else:
            return 0
```


### [909. 蛇梯棋](https://leetcode-cn.com/contest/weekly-contest-103/problems/snakes-and-ladders)

**思路：**

题目要求最小步数，所以用宽度优先搜索（Breadth First Search，BFS）来解决这个问题比较好，我们注意，路径中可能出现回路，但是出现回路肯定不是最优解，所以我们在搜索过程中，可以把搜索过的格子标记为 `0`，那么在下一层搜索过程中，只需要搜索值为 `-1` 或者大于 `0` 的格子即可。在搜索之前，我们可以将二维数组变为一位数组来简化搜索过程。

时间复杂度 $O(N^2)$

空间复杂度 $O(N^2)$


**代码：**
```python
class Solution:
    def snakesAndLadders(self, board):
        """
        :type board: List[List[int]]
        :rtype: int
        """
        n = len(board)
        road = []
        i = n - 1
        flg = True
        while i >= 0:
            if flg:
                road += board[i]
            else:
                road += board[i][::-1]
            flg = not flg
            i -= 1
        l = n * n
        ans = 0
        queue = [0]
        while queue:
            ans += 1
            if ans >= l:
                return -1
            tmp = []
            while queue:
                p = queue.pop(0)
                for i in range(1, 7):
                    next_p = p + i
                    if next_p == l - 1:
                        return ans
                    if road[next_p] > 0:
                        jump = road[next_p] - 1
                        if jump == l - 1:
                            return ans
                        # 走过梯子或蛇了
                        road[next_p] = 0
                        tmp.append(jump)
                    elif road[next_p] == -1:
                        tmp.append(next_p)
                        road[next_p] = 0
            queue = tmp
        return -1
```


### [910. 最小差值 II](https://leetcode-cn.com/contest/weekly-contest-103/problems/smallest-range-ii)

**思路：**

为了生成数组 `B`，将数组升序排序后，我们需要找到数组中的一个数，小于等于这个数都加上 `K`，大于这个数都减去 `K`，设这个数是第 `i` 个数，那么输出的结果为 `max(A[len(A)-1] - K, A[i] + K) - min(A[0] + K, A[i + 1] - K)`。

时间复杂度 $O(logN)$

空间复杂度 $O(1)$


**代码：**
```python
class Solution:
    def smallestRangeII(self, A, K):
        """
        :type A: List[int]
        :type K: int
        :rtype: int
        """
        l = len(A)
        if l <= 1:
            return 0
        A.sort()
        ans = A[l - 1] - A[0]
        for i in range(l - 1):
            ma = max(A[i] + K, A[l - 1] - K)
            mi = min(A[i + 1] - K, A[0] + K)
            ans = min(ans, ma - mi)
        return ans
```


### [911. 在线选举](https://leetcode-cn.com/contest/weekly-contest-103/problems/online-election)

**思路：**

以给的投票时间序列 `times` 为索引，记录每次投票后的胜出候选人，在查询的时候采用二分法即可在对数时间内返回正确结果。计算胜出候选人的时候，用 `hashmap` 记录每个候选人的票数，并用变量记录当前优胜者和最大票数，如果投票后，当前投给的候选人票数大于等于当前优胜者的票数，那么替换当前优胜者和最大票数。

构造时间复杂度 $O(N)$  查询时间复杂度 $O(logN)$

空间复杂度 $O(N)$


**代码：**
```python
class TopVotedCandidate:

    def __init__(self, persons, times):
        """
        :type persons: List[int]
        :type times: List[int]
        """
        l = len(times)
        self.t = times
        self.winner = [persons[0]] * l
        d = dict()
        winner_bynow = persons[0]
        max_ticket = 1
        d[persons[0]] = 1
        for i in range(1, l):
            if persons[i] in d:
                d[persons[i]] += 1
            else:
                d[persons[i]] = 1
            if d[persons[i]] >= max_ticket:
                winner_bynow = persons[i]
                max_ticket = d[persons[i]]
            self.winner[i] = winner_bynow
            
    def q(self, t):
        """
        :type t: int
        :rtype: int
        """
        index = bisect.bisect(self.t, t) - 1
        return self.winner[index]


# Your TopVotedCandidate object will be instantiated and called as such:
# obj = TopVotedCandidate(persons, times)
# param_1 = obj.q(t)
```


