Title: Some tips for configing the flume properties
Date: 2017-05-25 21:15
Tags: Flume,CDH,Centos
Category: Blog
Slug: Some-tips-for-configing-the-flume-prpperties
Author: zhoudshu

# The Tips

  [__Flume__](http://flume.apache.org/) is a distributed, reliable, and available service for efficiently collecting, aggregating, and moving large amounts of log data.I already have installed many flume systems to collect streaming log data. But I found some problems when we used flume. I write this blog to record the problems and solutions. and anybody else will avoid such problem.

## The running environment

* CDH version 5.8.0+
* Flume 1.6.0+
* Java 1.7.0+
* Linux 2.6.32-573.el6.x86_6
* Centos 6.6+

## Tips one :rotating invalid
  flume by using the following configuration uploads and rotates files to hadoop hdfs every 300 seconds, However, When filePrefix attribute is written by "access.log.228.%Y%m%d%H%M". the idleTimeout will be invalid and rotating file to hadoop hdfs will became 60 seconds.


```bash
tier1.sinks.sinkhdfs.type = hdfs
tier1.sinks.sinkhdfs.hdfs.path = hdfs://nameservice1/user/admin/data/%Y%m%d
tier1.sinks.sinkhdfs.hdfs.filePrefix = access.log.228.%Y%m%d%H
tier1.sinks.sinkhdfs.hdfs.writeFormat = Text
tier1.sinks.sinkhdfs.hdfs.fileType = CompressedStream
tier1.sinks.sinkhdfs.hdfs.codeC = gzip
tier1.sinks.sinkhdfs.hdfs.rollInterval = 300
tier1.sinks.sinkhdfs.hdfs.useLocalTimeStamp=true
tier1.sinks.sinkhdfs.hdfs.rollSize = 134217728
tier1.sinks.sinkhdfs.hdfs.rollCount = 0
tier1.sinks.sinkhdfs.hdfs.idleTimeout = 300
tier1.sinks.sinkhdfs.hdfs.minBlockReplicas=1
tier1.sinks.sinkhdfs.hdfs.callTimeout = 60000
tier1.sinks.sinkhdfs.hdfs.batchSize = 100

```
## Tips two : reload config
 Sometimes, We must reload flume process and do not restart flume

* to avoid losing the data in momery.
* to rotate tmp file to normal file

 We can not use the command "kill -9 " and use the command "kill". Flume can trap the signal and rotate the temporary file to normal file.

```bash
[root@xxxxxxxxxxxx ]# kill pid(flume process)

```

## Tips Three : disable auto reload feather
 Flume has one thread which can scan every the constant time if flume-conf.properties is modified and reload changed config file. But, Reloading config is invalid when we can change filePrefix attribute from "access.log.228.%Y%m%d%H%M" to "access.log.228.%Y%m%d%H". So We must forbid this function with --no-reload-conf parameter

```bash
nohup bin/flume-ng agent --conf /usr/local/flume/conf -f conf/flume-conf.properties -n tier1 -Dflume.monitoring.type=http -Dflume.monitoring.port=34545 --no-reload-conf  >/dev/null 2>&1 

```
## Tips Four : SPILLABLEMEMORY can lost data
 We use SPILLABLEMEMORY in channel of Flume to increase performance. it can lose the data when we restart flume. 


## Good luck
