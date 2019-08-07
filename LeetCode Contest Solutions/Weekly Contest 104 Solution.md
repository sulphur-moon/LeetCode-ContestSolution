## [第 104 场周赛](https://leetcode-cn.com/contest/weekly-contest-104)

本周比赛前三题较简单，但是最后一题较难，用到了极大极小算法。

### [914. 卡牌分组](https://leetcode-cn.com/contest/weekly-contest-104/problems/x-of-a-kind-in-a-deck-of-cards)

**思路：**

统计每个元素在 `deck` 中出现的次数，然后求这些次数的最大公约数，如果最大公约数为 `1`，则返回 `False`，否则返回 `True`。

时间复杂度 $O(Nlog^2N)$

空间复杂度 $O(N)$


**代码：**
```python
class Solution:
    def hasGroupsSizeX(self, deck):
        """
        :type deck: List[int]
        :rtype: bool
        """
        from collections import Counter
        import math
        d = Counter(deck)
        cnt = d.values()
        if min(cnt) == 1:
            return False
        cnt = list(cnt)
        ans = cnt[0]
        for i in range(1, len(cnt)):
            ans =  math.gcd(ans, cnt[i])
            if ans == 1:
                return False
        return True
```


### [915. 分割数组](https://leetcode-cn.com/contest/weekly-contest-104/problems/partition-array-into-disjoint-intervals)

**思路：**

用 `left[i]` 来表示 `i` 左边的最大值（包括 `i`），用 `right[i]` 来表示 `i` 右边的最小值（包括 `i`），那么我们只需要寻找一个最小的 `i`，使得 `left[i] <= right[i + 1]`。也有更简单的方法，用一次遍历，遍历到 `i` 时，当前答案为 `ans`，则 `ans` 初始值为 `1`。当我们从第二个元素开始遍历到第 `i` 个元素时，我们可以记录 `[0, ans - 1]` 中最大元素为 `leftMax`，记录 `[ans, i]` 中最大元素为 `rightMax`，当 `A[i] < leftMax` 时，证明之前的分割不合理，需要更新分割为 `ans = i + 1`。

时间复杂度 $O(N)$

空间复杂度 $O(N)$
**代码：**

两次遍历

```python
class Solution:
    def partitionDisjoint(self, A):
        """
        :type A: List[int]
        :rtype: int
        """
        l = len(A)
        left = [A[0]] * l
        right = [[A[l - 1]]] * l
        left_max = 0
        right_min = 1000000
        for i in range(l):
            left_max = max(left_max, A[i])
            left[i] = left_max
            right_min = min(right_min, A[l - i - 1])
            right[l - i - 1] = right_min
        for i in range(l - 1):
            if left[i] <= right[i + 1]:
                return i + 1
```

一次遍历

```python
class Solution:
    def partitionDisjoint(self, A):
        """
        :type A: List[int]
        :rtype: int
        """
        leftMax, rightMax = A[0], A[0]
        ans, n = 1, len(A)

        for i in range(1, n-1):
            if A[i] < leftMax:  
                ans = i + 1  # 更新分割线
                if rightMax > leftMax:
                    leftMax = rightMax
            elif A[i] > rightMax:
                rightMax = A[i]

        return ans
```
### [916. 单词子集](https://leetcode-cn.com/contest/weekly-contest-104/problems/word-subsets)

**思路：**

对 `B` 中的每个单词统计字母出现次数，然后建一个 `counter` 来统计每个字母在 `B` 中出现次数的最大值（相当于取并集，也就是下面第二个写法里每次计算差集再相加）。最后判断 `A` 中的每个单词是否满足 `counter` 即可。


**代码：**

```python
class Solution:
    def wordSubsets(self, A, B):
        """
        :type A: List[str]
        :type B: List[str]
        :rtype: List[str]
        """
        # make dict
        dict_A = []
        dict_B = []
        for s in A:
            d = dict()
            for c in s:
                if c in d:
                    d[c] += 1
                else:
                    d[c] = 1
            dict_A.append(d)
        for s in B:
            d = dict()
            for c in s:
                if c in d:
                    d[c] += 1
                else:
                    d[c] = 1
            dict_B.append(d)
        # union dict_B
        judger = dict()
        for d in dict_B:
            for c in d:
                if c not in judger or judger[c] < d[c]:
                    judger[c] = d[c]
                    
        # judge if d1 is subset of d2
        def isSub(d1, d2):
            for k in d1:
                if k not in d2 or d1[k] > d2[k]:
                    return False
            return True
        
        # cal ans
        ans = []
        for i in range(len(A)):
            if isSub(judger, dict_A[i]):
                ans.append(A[i])
        return ans
```

更简单的写法

```python
class Solution:
    def wordSubsets(self, A, B):
        """
        :type A: List[str]
        :type B: List[str]
        :rtype: List[str]
        """
        union_B = []
        ans = []
        for b in B:
            dict_B = union_B.copy()
            for i in b:
                if i in dict_B:
                    dict_B.remove(i)
                else:
                    union_B.append(i)
                    
        for a in A:
            ok = True
            i = list(a)
            for j in union_B:
                if j in i:
                    i.remove(j)
                else:
                    ok = False
                    break
            if ok:
                ans.append(a)
        return ans
```


### [913. 猫和老鼠](https://leetcode-cn.com/contest/weekly-contest-104/problems/cat-and-mouse)

**思路：**

极小极大算法。

游戏的状态可以表示为 `(m, c, t)` 其中`m` 代表老鼠的位置，`c` 代表猫的位置，`t` 为 `1` 轮到老鼠，为`2`时轮到猫。然后我们可以把每个状态看做是一张有向图里的结点。其中有些结点已经有了结果，如果老鼠进了洞 `(m = 0)`，则老鼠赢；如果猫抓到老鼠 `(c = m)`，则猫赢。然后让我们对图的结点进行染色，结点存在三种状态，要么老鼠赢，要么猫赢，要么平局，我们先把未解出的结点全都标记为平局。在极小极大算法里，老鼠会优先选择自己赢得结点，其次是平局，最后才是猫赢；而猫的策略正好相反。

我们对未解出的平局结点 `node` 进行染色，应遵守以下规则（我们假设该结点 `node` 是老鼠的回合 `node.turn = Mouse`，猫的回合同理）：

- 直接染色：如果一个结点的儿子中，有一个被标记为老鼠赢，那么该结点就标记为老鼠赢；
- 最终染色：如果一个结点的所有儿子都是猫赢，那么这个结点就标记为猫赢。

我们重复执行上述规则对这个有向图进行染色，直到没有结点符合以上染色规则为止。为了提高染色效率，我们采用一个队列来实现这个自底向上的过程：

- 将所有已解出的结点加入队列 （老鼠在洞里或者猫抓住老鼠的情况）
- 对队列中的每个结点 `node` 枚举它们的父结点 `parent` ：
  - 如果可能，对父结点 `parent` 进行直接染色，例如`node`为老鼠赢，而它的一个父结点`parent`刚好是老鼠回合，那么这个`parent`就直接标记为老鼠赢，并加入队列中；
  - 如果不能，例如`node`为猫赢，它的一个父节点`parent`是老鼠回合，那么我们就将这个父结点的出度减`1`，那么如果一个结点的出度降为`0`，那么也就说明了，这个结点所有子结点都是输，这样就可以对这个结点进行最终染色，标记为输，并加入队列中。


**代码：**
```python
class Solution:
    def catMouseGame(self, graph):
        """
        :type graph: List[List[int]]
        :rtype: int
        """
        N = len(graph)

        # What nodes could play their turn to
        # arrive at node (m, c, t) ?
        def parents(m, c, t):
            if t == 2:
                for m2 in graph[m]:
                    yield m2, c, 3-t
            else:
                for c2 in graph[c]:
                    if c2:
                        yield m, c2, 3-t

        DRAW, MOUSE, CAT = 0, 1, 2
        color = collections.defaultdict(int)

        # degree[node] : the number of neutral children of this node
        degree = {}
        for m in range(N):
            for c in range(N):
                degree[m,c,1] = len(graph[m])
                degree[m,c,2] = len(graph[c]) - (0 in graph[c])

        # enqueued : all nodes that are colored
        queue = collections.deque([])
        for i in range(N):
            for t in range(1, 3):
                color[0, i, t] = MOUSE
                queue.append((0, i, t, MOUSE))
                if i > 0:
                    color[i, i, t] = CAT
                    queue.append((i, i, t, CAT))

        # percolate
        while queue:
            # for nodes that are colored :
            i, j, t, c = queue.popleft()
            # for every parent of this node i, j, t :
            for i2, j2, t2 in parents(i, j, t):
                # if this parent is not colored :
                if color[i2, j2, t2] is DRAW:
                    # if the parent can make a winning move (ie. mouse to MOUSE), do so
                    if t2 == c: # winning move
                        color[i2, j2, t2] = c
                        queue.append((i2, j2, t2, c))
                    # else, this parent has degree[parent]--, and enqueue if all children
                    # of this parent are colored as losing moves
                    else:
                        degree[i2, j2, t2] -= 1
                        if degree[i2, j2, t2] == 0:
                            color[i2, j2, t2] = 3 - t2
                            queue.append((i2, j2, t2, 3 - t2))

        return color[1, 2, 1]
```
