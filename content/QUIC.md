Title: QUIC阅读
Date: 2016-03-21 10:01
Category: Protocol
Tags: Protocol, QUIC
Slug: QUIC
Author: qingluck
Summary: Note for QUIC.
Comment: off

### 什么是HTTP Pipeline？
HTTP管线化是将多个HTTP请求（request）整批提交的技术，而在传送过程中不需先等待服务端的回应。管线化机制须通过永久连接（persistent connection）完成，仅HTTP/1.1支持此技术（HTTP/1.0不支持），并且只有GET和HEAD要求可以进行管线化，而POST则有所限制。此外，初次创建连接时也不应启动管线机制，因为对方（服务器）不一定支持HTTP/1.1版本的协议。
浏览器将HTTP请求大批提交可大幅缩短页面的加载时间，特别是在传输延迟（lag/latency）较高的情况下（如卫星连接）。此技术之关键在于多个HTTP的请求消息可以同时塞入一个TCP分组中，所以只提交一个分组即可同时发出多个请求，借此可减少网络上多余的分组并降低线路负载。

### 什么是复用流（Multiplexed Stream）？
假设两种火车代表不同的流，如下图：

然后，将它们排在一个连接上进行传输，如同行驶在单个铁轨上一样：


HTTP2连接可以承载数十或数百个流的复用，多路复用意味著来自很多流的数据包能够混合在一起通过同样连接传输，两列不同火车被混合在一起传输，当到达终点时，它们又被拆开组成两列不同的火车。

### 为什么要使用复用流（Mutiplexed Stream）？
* 减少端口使用
* 对网络通道状况（如丢包）进行统一报告和响应
* 有利于减少应用层的数据冗余性
* 在服务器负载均衡的情况下，保证客户端由同一个服务器服务

### 什么是packet pacing?
该机制用于减少数据传输的突发性，数据传输的突发性容易导致数据包丢失[1,2]

### decrease the number of round trips
To continue improving network performance we need to decrease the number of round trips, something that is difficult with protocols that currently rely on the Transmission Control Protocol (TCP).[3]

### 什么是*serialization latency*
根据[4]，相关概念有*packetization delay*和*propagation delay* 。

***serialization latency***即为序列化时延，数据分组从网卡到网线上所产生的时延。
> serialization delay, the delay in moving packets from the Network Interface Controller’s (NIC) transmit buffer to the wire.

序列化时延公式如下：
>Serialization Delay = Size of Packet (bits) / Transmission Rate (bps)

由此可见，序列化时延即发送时延*transmission delay*

***packetization  delay***
>This delay refers to the time it takes a system to create and fill packets of data for sending over internet protocol related technologies.

***propagation delay***即为传播时延，与传输介质有关。
>propagation delay, the latency of these packets as they travel between the sending and receiving nodes.

[1][https://en.wikipedia.org/wiki/TCP_pacing](https://en.wikipedia.org/wiki/TCP_pacing)

[2][https://fasterdata.es.net/host-tuning/packet-pacing](https://fasterdata.es.net/host-tuning/packet-pacing)

[3][http://blog.chromium.org/2013/06/experimenting-with-quic.html](http://blog.chromium.org/2013/06/experimenting-with-quic.html)

[4][https://techdoertimes.wordpress.com/2007/11/01/measuring-latency-serialization-delay/](https://techdoertimes.wordpress.com/2007/11/01/measuring-latency-serialization-delay/)
