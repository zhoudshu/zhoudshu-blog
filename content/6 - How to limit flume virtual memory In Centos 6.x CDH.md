Title: How to limit virtual memory using of Flume process in Centos 6.x
Date: 2017-04-06 21:15
Tags: Flume,CDH,virtual,Memory,Centos
Category: Blog
Slug: How-to-limit-virtual-memory-using-of-Flume-process-in-CentOs-6.x
Author: zhoudshu

# The Problem

  [__Flume__](http://flume.apache.org/) is a distributed, reliable, and available service for efficiently collecting, aggregating, and moving large amounts of log data.I already have installed many flume systems to collect streaming log data. But I found one problem that flume process was occuping more virtual memories and fewer physical memories. Why is this situation occurred? This blog explains and provides the methods to solve this problem. 

## The running environment

* CDH version 5.8.0+
* Flume 1.6.0+
* Java 1.7.0+
* Linux 2.6.32-573.el6.x86_6
* Centos 6.6+

## The Top command Result of flume process
```bash
26963 root      20   0 15.3g 2.3g  27m S  0.3  3.7  32:21.32 java                                                                                                       
28006 root      20   0 15216 2308 1800 R  0.3  0.0   0:00.02 top                                                                                                        
    1 root      20   0 19292 1324 1052 S  0.0  0.0   0:05.87 init                                                                                                       
    2 root      20   0     0    0    0 S  0.0  0.0   0:05.69 kthreadd                                                                                                   
    3 root      20   0     0    0    0 S  0.0  0.0  27:17.09 ksoftirqd/0                                                                                                
    5 root       0 -20     0    0    0 S  0.0  0.0   0:00.00 kworker/0:0H                                                                                               
    9 root      20   0     0    0    0 S  0.0  0.0   0:00.00 rcu_bh                                                                                                     
   10 root      20   0     0    0    0 S  0.0  0.0 246:51.36 rcuos/0                                                                                                    
   11 root      20   0     0    0    0 S  0.0  0.0   0:00.00 rcuob/0                                                                                                    
   12 root      RT   0     0    0    0 S  0.0  0.0   0:27.36 migration/0                                                                                                
   13 root      RT   0   

```
## The Result of Pmap command

```bash
[root@xxxxxxxxxxxx ]# pmap  26963|grep anon|more
000000000130b000    132K rw---    [ anon ]
00000005c0000000 2796544K rw---    [ anon ]
000000066ab00000 2796032K -----    [ anon ]
0000000715580000 1968640K rw---    [ anon ]
000000078d800000 827392K -----    [ anon ]
00000007c0000000   4784K rw---    [ anon ]
00000007c04ac000 1043792K -----    [ anon ]
00007fa5b0000000   2020K rw---    [ anon ]
00007fa5b01f9000  63516K -----    [ anon ]
00007fa5b4000000   1416K rw---    [ anon ]

```

## The Reason 
  In Linux, starting with GLIBC Version 2.10 and higher, a new feature has emerged to help address memory locations and proximity to processor cores. Prior to this feature, everything stayed within one memory pool, so the data did not get closer to the cores. Now, this functionality assists processes by bringing the data closer to the processor currently utilizing the information.  By default, the total number of pools equal 64; thus, there are many 'buckets' to which the data can move.  However, we have discovered that when fully utilized in CentOS/RHEL 6.x, this functionality can also generate negative side effects especially in large-scale implementations of Infobright.

## The solution of Flume which are run alone
  In file flume-env.sh, We can add the following MALLOC_ARENA_MAX line to fix this problem

```bash
export JAVA_HOME=/usr/lib/jvm/java-openjdk

# Give Flume more memory and pre-allocate, enable remote monitoring via JMX
export JAVA_OPTS="-Xms4g -Xmx8g -Dcom.sun.management.jmxremote"

# Note that the Flume conf directory is always included in the classpath.
#FLUME_CLASSPATH=""

export MALLOC_ARENA_MAX=1

```

## The solution of Flume in CDH
  From CDH cmf services, I can configure java environment options of flume agent
```bash

MALLOC_ARENA_MAX=1

```

## Good luck
