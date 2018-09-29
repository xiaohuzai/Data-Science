# HDFS(一) HDFS架构

### 一、HDFS架构

![](https://raw.githubusercontent.com/xiaohuzai/Data-Science/master/HADOOP/pictures/HDFS/1.png)

HDFS是一个**Master/Slave**架构。

完整的HDFS有：

- 一个Namenode进程，负责文件系统的名称空间以及控制客户端的访问请求。

- 多个Datanode进程，集群中每一个物理节点即一个Datanode，由其管理服务器上的物理存储空间。


Nmaenode通过特定的RPC文件系统来实现文件的打开、关闭、重命名等操作。同时也维持着文件名和存储在不同的Datanode上数据块的映射。

Datanode可以响应客户端的读写请求，也接受来自Namenode的数据块创建、删除、复制等等。

**Namenode**（管理节点），即Master

- 负责名称空间的管理，所有的文件系统的管理
- 负责文件到数据块的映射，以及数据块和存储节点对应关系

**DataNode**（数据存储节点）

- 向管理节点汇报数据块信息
- 存储节点之间通过复制操作来实现数据均衡和备份
- 与客户端交互，执行数据读写请求

**Client**（客户端）

- 向NN/DN发起读写请求

**Rack**（机架）

- 存储节点放在不同的机架上，这与数据备份策略有关系

**Blocks**（数据块）

- 数据切分成了特定大小的数据块，分发到不同的存储节点

**Replication**（副本）

- 数据块在不同的存储节点之间，通过复制的方式来拷贝。副本是HDFS实现高可用的核心实现。

### 二、HDFS读写流程

**HDFS读流程**：

![](https://raw.githubusercontent.com/xiaohuzai/Data-Science/master/HADOOP/pictures/HDFS/2.png)

1. 客户端向NN发起读请求，会请求一个文件；
2. NN返回请求文件的数据块所在的存储节点列表，如果该文件有多个数据块，则返回多个数据列表；
3. 客户端根据返回的节点列表，优先选择最近的节点访问；
4. 客户端直接与DN节点连接读取相应的Block数据，读完这个Block后关闭连接。若该文件有多个数据块，客户端会选择下一个block的所在节点，进行连接，重复上述过程。
5. 当读完最后一个数据块，客户端关闭连接，



**HDFS写流程：**

![](https://raw.githubusercontent.com/xiaohuzai/Data-Science/master/HADOOP/pictures/HDFS/3.png)

1. 客户端会发起请求 
2. DF向NN生成一个文件路径。NN会返回这个文件第一个Blocks所在的DN列表信息
3. 客户端根据返回的DN列表，回选取离它最近的节点，创建Socket连接
4. 接着第一个节点与第二个节点、第二个节点与第三个节点，会顺序构建Socket连接，形成一个数据管道，然后客户端会向第一个节点发起数据传输，当第一个节点收到数据传输后，会顺序向第二个节点发送数据，第二个会向第三个节点发送，在第三个数据收到后，会把数据的Ack信息发回到第二个节点。第二个再发送给第一个节点
5. 第一个节点收到Ack信息后，会把Ack信息传给客户端。客户端在确认Ack后，才认为数据传输成功，开始下一个数据的传输。循环往复完成整个Block的写操作。在第一个Block写操作完成之后，如果这个文件还有数据要传输，客户端会申请新的Block，客户端会重新创建一个新的DN数据管道，来进行数据传输。

### 三、HDFS的副本放置策略

由NN来选择放置副本。以三副本为例。

在与客户端相同的节点上放置第一个副本，第二个副本放置在与第一个副本不同的随机选择的机架上，第三个副本放置在第二个相同的机架上，但是不同节点。

![](https://raw.githubusercontent.com/xiaohuzai/Data-Science/master/HADOOP/pictures/HDFS/4.png)

客户端是如何选择读取哪个副本的呢？

​	是靠定义不同存储位置的距离，然后NN根据可用blocks的距离排序，选择最近的节点来读取的。

对存储位置的定义：

![](https://raw.githubusercontent.com/xiaohuzai/Data-Science/master/HADOOP/pictures/HDFS/5.png)

