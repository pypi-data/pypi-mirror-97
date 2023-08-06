# trdb2py

这是 ``tradingdb2`` 的python库，初衷是希望有一个更方便的研究工具，能在 ``jupyter`` 里使用。

大量的运算，都是通过 ``tradingdb2`` 发送给 ``tradingnode2`` 节点进行分布式运算，而 ``tradingdb2`` 负责负载均衡 和 结果缓存，这样就算 ``jupyter`` 有什么问题，也不至于要重新运算。

图形化选择的是 ``plotly`` 。

# 安装

直接用 ``pip`` 安装即可。

```
pip install trdb2py
```

# 更新日志

### v0.2

- 加入更多本地分析功能，不会把所有计算都放云端。

### v0.1

- 实现了基本功能。

