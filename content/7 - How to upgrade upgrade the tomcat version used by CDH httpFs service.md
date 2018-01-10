Title: How to upgrade the tomcat version used by CDH httpFs service 
Date: 2017-04-06 21:45
Tags: Tomcat,CDH,HttpFs,security,Bug
Category: Blog
Slug: How-to-upgrade-the-tomcat-version-used-by-CDH-httpFs-service
Author: zhoudshu

# The Problem

  [__Tomcat__](https://tomcat.apache.org/security-6.html) released one patch which fixed one error bug about CVE-2016-8745. In my CDH cluster, httpFS service is used by web http service, and it is run by 6.0.44 version Tomcat. We must upgrade the tomcat version from 6.0.44 to 6.0.50+ avoid of security attacking.

## the CDH Envirenment

* CDH version 5.7.0+
* Java 1.7.0+
* Linux 2.6.32-573.el6.x86_6
* Centos 6.6+

## The upgrade steps
### Download the newest version of tomcat

  [__Tomcat version 6.0.53__](http://mirror.bit.edu.cn/apache/tomcat/tomcat-6/v6.0.53/bin/apache-tomcat-6.0.53.tar.gz) can be downloaded. I can extract gz package

```bash

tar xvfz apache-tomcat-6.0.53.tar.gz
```

### Backup the old version for rollback
```bash
#cd /opt/cloudera/parcels/CDH/lib/bigtop-tomcat/
#cp -rf lib lib.6.0.44
```

### override the jar package 
```bash

cp $apache-tomcat-6.0.53/lib/* lib/

```

### Restart the httpfs service in cmf web 

## Good luck
