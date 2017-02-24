Title: Flume must be used the hadoop native libraries when uploading gz file 
Date: 2016-12-27 18:15
Tags: Flume,hadoop,gzip,compress,native
Category: Blog
Slug: Flume-must-be-used-the-hadoop-native-libraries 
Author: zhoudshu

# THe Problem

Recently, I had been one requirement in my project for uploading real-time log record into hadoop cluster. I chose the open source software [__Flume__](https://flume.apache.org/). After installing flume, The log record could be transferred to hadoop cluster with gz suffix successfully. But I found the gz file size more than decompressed one. 

```bash
-rw-r--r-- 1 root   root        942 Dec 27 17:28 ngaancache-access.log.2016122321.1482498035352
-rw-r--r-- 1 root   root       6571 Dec 27 17:32 ngaancache-access.log.2016122321.1482498035352.gz

```

When I used gzip command to decompress this file, one warning infomation "trailing garbage ignored" is reported as followed

```bash
#gzip -d testcache-access.log.2016122321.1482498035352.gz

#gzip: testcache-access.log.2016122321.1482498035352.gz: decompression OK, trailing garbage ignored

```

At the same time, When I used spark software to read this file, One error was occured

```bash
16/12/14 01:10:33 WARN scheduler.TaskSetManager: Lost task 60.0 in stage 0.0 (TID 57, hadoop2): java.io.IOException: incorrect header check
        at org.apache.hadoop.io.compress.zlib.ZlibDecompressor.inflateBytesDirect(Native Method)
        at org.apache.hadoop.io.compress.zlib.ZlibDecompressor.decompress(ZlibDecompressor.java:228)
        at org.apache.hadoop.io.compress.DecompressorStream.decompress(DecompressorStream.java:91)
        at org.apache.hadoop.io.compress.DecompressorStream.read(DecompressorStream.java:85)
        at java.io.InputStream.read(InputStream.java:101)
        at org.apache.hadoop.util.LineReader.fillBuffer(LineReader.java:180)
        at org.apache.hadoop.util.LineReader.readDefaultLine(LineReader.java:216)
        at org.apache.hadoop.util.LineReader.readLine(LineReader.java:174)
        at org.apache.hadoop.mapred.LineRecordReader.next(LineRecordReader.java:248)
        at org.apache.hadoop.mapred.LineRecordReader.next(LineRecordReader.java:48)
        at org.apache.spark.rdd.HadoopRDD$$anon$1.getNext(HadoopRDD.scala:246)
        at org.apache.spark.rdd.HadoopRDD$$anon$1.getNext(HadoopRDD.scala:208)
        at org.apache.spark.util.NextIterator.hasNext(NextIterator.scala:73)
        at org.apache.spark.InterruptibleIterator.hasNext(InterruptibleIterator.scala:39)
        at scala.collection.Iterator$$anon$11.hasNext(Iterator.scala:327)
        at scala.collection.Iterator$$anon$14.hasNext(Iterator.scala:388)
        at scala.collection.Iterator$$anon$11.hasNext(Iterator.scala:327)
        at scala.collection.Iterator$$anon$14.hasNext(Iterator.scala:388)
        at scala.collection.Iterator$$anon$11.hasNext(Iterator.scala:327)
        at org.apache.spark.shuffle.sort.BypassMergeSortShuffleWriter.write(BypassMergeSortShuffleWriter.java:148)
        at org.apache.spark.scheduler.ShuffleMapTask.runTask(ShuffleMapTask.scala:73)
        at org.apache.spark.scheduler.ShuffleMapTask.runTask(ShuffleMapTask.scala:41)
        at org.apache.spark.scheduler.Task.run(Task.scala:89)
        at org.apache.spark.executor.Executor$TaskRunner.run(Executor.scala:214)
        at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1145)
        at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:615)
        at java.lang.Thread.run(Thread.java:745)
```

# Solved Method
By using google, I learns we must use hadoop native libraries for compressing gz format. In my CDH5.8.2 hadoop, I found the native libraries

```bash
ll /opt/cloudera/parcels/CDH-5.8.2-1.cdh5.8.2.p0.3/lib/hadoop/lib/native/
total 2132
-rw-r--r-- 1 root root  222050 Sep 12 04:24 libhadoop.a
-rw-r--r-- 1 root root  193092 Sep 12 04:24 libhadooppipes.a
lrwxrwxrwx 1 root root      18 Oct  9 16:30 libhadoop.so -> libhadoop.so.1.0.0
-rwxr-xr-x 1 root root  139296 Sep 12 04:24 libhadoop.so.1.0.0
-rw-r--r-- 1 root root   58600 Sep 12 04:24 libhadooputils.a
-rw-r--r-- 1 root root   99766 Sep 12 04:24 libhdfs.a
-rw-r--r-- 1 root root 1002468 Sep 12 04:24 libnativetask.a
lrwxrwxrwx 1 root root      22 Oct  9 16:30 libnativetask.so -> libnativetask.so.1.0.0
-rwxr-xr-x 1 root root  421912 Sep 12 04:24 libnativetask.so.1.0.0
lrwxrwxrwx 1 root root      18 Oct  9 16:30 libsnappy.so -> libsnappy.so.1.1.3
lrwxrwxrwx 1 root root      18 Oct  9 16:30 libsnappy.so.1 -> libsnappy.so.1.1.3
-rwxr-xr-x 1 root root   23904 Sep 12 04:24 libsnappy.so.1.1.3
 
```
I copy this files to flume plugin.d directory, restart flume and this problem is solved:

```bash
#ll plugins.d/hadoop/*

plugins.d/hadoop/native:
total 2132
-rw-r--r-- 1 root root  222050 Dec 22 11:23 libhadoop.a
lrwxrwxrwx 1 root root      18 Dec 23 14:04 libhadoop.so -> libhadoop.so.1.0.0
-rwxr-xr-x 1 root root  139296 Dec 22 11:23 libhadoop.so.1.0.0
-rw-r--r-- 1 root root  193092 Dec 22 11:23 libhadooppipes.a
-rw-r--r-- 1 root root   58600 Dec 22 11:23 libhadooputils.a
-rw-r--r-- 1 root root   99766 Dec 22 11:23 libhdfs.a
-rw-r--r-- 1 root root 1002468 Dec 22 11:23 libnativetask.a
lrwxrwxrwx 1 root root      22 Dec 23 14:04 libnativetask.so -> libnativetask.so.1.0.0
-rwxr-xr-x 1 root root  421912 Dec 22 11:23 libnativetask.so.1.0.0
lrwxrwxrwx 1 root root      18 Dec 23 14:04 libsnappy.so -> libsnappy.so.1.1.3
lrwxrwxrwx 1 root root      18 Dec 23 14:04 libsnappy.so.1 -> libsnappy.so.1.1.3
-rwxr-xr-x 1 root root   23904 Dec 22 11:23 libsnappy.so.1.1.3

# the installed environment 

* Linux OS: CentOS 6.7 2.6.32-573.el6.x86_64
* Flume: 1.6.0
* CDH  : 5.8.2-1.cdh5.8.2.p0.3
# Java : 1.8.0

# Flume config file content

```bash
a1.sources = r1
a1.sinks = k1
a1.channels = c1

a1.sources.r1.type =exec
a1.sources.r1.command=tail -F /home/test/testflume/logs/flume.log

a1.sinks.k1.type= hdfs
a1.sinks.k1.hdfs.useLocalTimeStamp= true

a1.sinks.k1.hdfs.path= hdfs://hadoop1:8020/user/root/testflume/%Y-%m-%d 
a1.sinks.k1.hdfs.writeFormat = Text

a1.sinks.k1.hdfs.useLocalTimeStamp = true
a1.sinks.k1.hdfs.fileType = CompressedStream
a1.sinks.k1.hdfs.codeC = gzip
a1.sinks.k1.hdfs.minBlockReplicas= 1

a1.sinks.k1.hdfs.rollInterval= 50
a1.sinks.k1.hdfs.rollSize= 0
a1.sinks.k1.hdfs.rollCount= 0
a1.sinks.k1.hdfs.idleTimeout= 0

a1.channels.c1.type = memory
a1.channels.c1.capacity = 1000000
a1.channels.c1.transactionCapacity = 1000000

a1.sources.r1.channels = c1
a1.sinks.k1.channel = c1

```
