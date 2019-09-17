## [第 154 场周赛](https://leetcode-cn.com/contest/weekly-contest-154)

本周比赛考察了数学统计、栈、队列、动态规划、Tarjan求割边等算法。

### [1189. “气球” 的最大数量](https://leetcode-cn.com/contest/weekly-contest-154/problems/maximum-number-of-balloons)

**思路：**

统计一下字符串中每个字符出现的频次，然后看有多少个 `b`，`a`，`l`，`o`，`n` 即可。根据木桶原理，取最小的那个数字，记得 `l` 和 `o` 的个数要除以 2。


**代码：**
```python
class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        cnt = collections.Counter(text)
        return min(cnt['b'], cnt['a'], cnt['l'] // 2, cnt['o'] // 2, cnt['n'])
```


### [1190. 反转每对括号间的子串](https://leetcode-cn.com/contest/weekly-contest-154/problems/reverse-substrings-between-each-pair-of-parentheses)

**思路：**

根据题意

1. 当遇到左括号 `'('` 时，栈中新加入一个空字符串；
2. 当遇到字符的时候，把字符追加进栈顶字符串中；
3. 当遇到右括号 `')'` 时，将栈顶字符串弹出反转，并将弹出的字符串追加到栈顶的字符串。

其实这是一个栈套栈的结构，这里只不过是用字符串的反转代替了括号内字符全部入栈再全部出栈的操作。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1190-1.gif)


**代码：**
```python
class Solution:
    def reverseParentheses(self, s: str) -> str:
        stack = ['']
        for c in s:
            if c == '(':
                stack.append('')
            elif c == ')':
                add = stack.pop()[::-1]
                stack[-1] += add
            else:
                stack[-1] += c
        return stack.pop()
```


### [1191. K 次串联后最大子数组之和](https://leetcode-cn.com/contest/weekly-contest-154/problems/k-concatenation-maximum-sum)

**思路：**

分三种情况：

1. 当 k == 1 时，直接用动态规划求子数组最大和并返回答案；
2. 当 k > 1 时，我们求该数组的最大前缀和与最大后缀和，由于数组拼接多次，那么最大前缀和和最大后缀和可以组成一个和更大的子数组；
3. 当 k > 1并且数组和 s > 0 时，答案就是全部数组都用到，第一个数组用最大后缀和，最后一个数组用最大前缀和。

**图解：**

![图解](http://qiniu.wenyuetech.cn/1191-1.png)


**代码：**
```python
class Solution:
    def kConcatenationMaxSum(self, arr: List[int], k: int) -> int:
        mod = 10 ** 9 + 7
        curr_max = 0
        result_max = 0
        s = sum(arr)
        for num in arr:
            curr_max += num
            if curr_max <= 0:
                curr_max = 0
            if curr_max > result_max:
                result_max = curr_max
        if k == 1:
            return result_max % mod
        presum, premax = 0, 0
        sufsum, sufmax = 0, 0
        n = len(arr)
        for i in range(n):
            presum += arr[i]
            premax = max(premax, presum)
            sufsum += arr[n - i - 1]
            sufmax = max(sufmax, sufsum)
        loopmax = premax + sufmax + s * (k - 2)
        ans = max(premax + sufmax, loopmax, result_max)
        return ans % mod
```


### [1192. 查找集群内的「关键连接」](https://leetcode-cn.com/contest/weekly-contest-154/problems/critical-connections-in-a-network)

**思路：**

这是一道求无向图割边（即桥）的裸题，用 Tarjan 算法求解。

**桥（割边）：**无向连通图中，去掉一条边，图中的连通分量数增加，则这条边，称为桥或者割边。

下面简述一下 Tarjan 算法的原理：

用深度优先搜索（DFS）遍历图，在遍历过程中，我们定义三个数组：`dfn[i]` 表示结点 `i` 是第几个被遍历的（即访问顺序），这样，子结点的数值一定大于其父结点；`low[i]` 表示结点 `i` 不通过其父节点能访问的结点编号的最小值；`parent[i]` 表示结点 `i` 的父结点编号。遍历一遍后，如果 `low[v] > dnf[u] ` 就说明 V-U 是桥。


**代码：**
```python
class Solution:
    def criticalConnections(self, n: int, connections: List[List[int]]) -> List[List[int]]:
        INF = float('inf')
        graph = collections.defaultdict(list)
        for u, v in connections:
            graph[u].append(v)
            graph[v].append(u)
        visited = [False] * n
        dfn = [INF] * n
        low = [INF] * n
        parent = [-1] * n
        self.Time = 0
        ans = []
        
        def dfs(u, visited, parent, low, dfn): 
            visited[u]= True
            dfn[u] = self.Time 
            low[u] = self.Time 
            self.Time += 1
            for v in graph[u]: 
                if visited[v] == False : 
                    parent[v] = u 
                    dfs(v, visited, parent, low, disc) 
                    low[u] = min(low[u], low[v]) 
                    if low[v] > dfn[u]: 
                        ans.append([v, u])
                elif v != parent[u]:
                    low[u] = min(low[u], dfn[v]) 
                    
        for i in range(n):
            if not visited[i]:
                dfs(i, visited, parent, low, dfn)
        return ans
```


