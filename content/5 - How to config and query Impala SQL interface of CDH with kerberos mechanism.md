Title: How to config and query Impala SQL interface of CDH with kerberos mechanism
Date: 2017-02-23 21:55
Tags: Impala,CDH,kerberos,SQL,ldap
Category: Blog
Slug: How-to-config-and-impala-sql-interface-with-kerberos 
Author: zhoudshu

# The Problem

  Recently, I have spended several days on rearching impala sql interface with security mechanism. There are two methods to query impala data. One is the kerberos mechanism, the other is ldap method which provided user and password. The first one is very difficult and usually adapted for internal using in the hadoop cluster, So I choose the ldap method for external appliction such as jdbc interface. This blog provides the configuration steps and queries demo for using ldap to impala databases. 

## The test environment

* CDH version 5.8.0+
* kerberos software
* ldap service
* Linux 2.6.32-573.el6.x86_6
* Python 2.6.6+
* Java 1.7.0+

## Install Steps 

### Step 1: Install CDH Version
  There is a lot of paper or documents to install CDH on the internet. So we can google or bing it by "CDH install" keywords

### Step 2: Install the kerberos component in CDH
  There is official link [__CDH kerberos__](https://www.cloudera.com/documentation/enterprise/latest/topics/cm_sg_intro_kerb.html) 

### Step 3: Install and config Ldap server
  I use [__openldap__](http://www.openldap.org/) to build the ldap server and create one user ldaptest for test

### Step 4: Config Impala for supporting ldap
* enable_ldap_auth true
* ldap_uri ldap://ldap_ip:389
* ldap_bind_pattern mail=#UID@xxxx.com.cn,virtualDomain=xxx.com.cn,o=extmailAccount,dc=xxxx,dc=com
* Impala Daemon advanced parameters -ldap_passwords_in_clear_ok=true
 I config the above impala parameters and restart impala service

### Step 5: Python client for quering impala
 CDH suggestes using the [__impyla__](https://github.com/cloudera/impyla impyla) to visit the impala databases. First We must install the following yum package:
```bash
#yum install cyrus-sasl-plain cyrus-sasl cyrus-sasl-lib cyrus-sasl-devel cyrus-sasl-gssapi
#yum install gcc-c++ python-devel.x86_64 cyrus-sasl-devel.x86_64
#pip install thrift_sasl 
#pip install sasl

```
if you use the Python 2.6.6 version, you maybe find this error "AttributeError: 'TSaslClientTransport' object has no attribute "
the solution is used the low version thrift==0.9.3
```bash
pip uninstall thrift==0.10.0
pip install thrift==0.9.3
```

Python client demo source code file [__TestImpalaByLdap.py__](https://github.com/zhoudshu/testcode)

```python
from impala.dbapi import connect
import traceback 
try:
    conn   = connect(host='10.10.100.53', port=21050, auth_mechanism="PLAIN", \
                     user='ldaptest', password='xxxxx')
    cursor = conn.cursor()
    #sql     = "select * from mydb.test"
    sql      = "show databases;"
    cursor.execute(sql)
    print cursor.fetchall()
except:
    traceback.print_exc()
```
The executed result:

```bash
#python TestImpalaByLdap.py

[('_impala_builtins', 'System database for Impala builtin functions'), ('cdnportal', ''), ('default', 'Default Hive database'), ('dfdsdb', ''), ('mydb_impala', ''), ('portal', '')]
 
```

Note the parameter auth_mechanism of python [__TestImpalaError.py__](https://github.com/zhoudshu/testcode) connect fuction must not be "LDAP" , otherwise report the following error:

```python
  def connect(host='localhost', port=21050, database=None, timeout=None,
            use_ssl=False, ca_cert=None, auth_mechanism='NOSASL', user=None,
            password=None, kerberos_service_name='impala', use_ldap=None,
            ldap_user=None, ldap_password=None, use_kerberos=None,
            protocol=None):
   ....
   auth_mechanism : {'NOSASL', 'PLAIN', 'GSSAPI', 'LDAP'}
        Specify the authentication mechanism. `'NOSASL'` for unsecured Impala.
        `'PLAIN'` for unsecured Hive (because Hive requires the SASL
        transport). `'GSSAPI'` for Kerberos and `'LDAP'` for Kerberos with
        LDAP.
    user : str, optional
        LDAP user, if applicable.
    password : str, optional
        LDAP password, if applicable.
   ....
```

```bash
Traceback (most recent call last):
  File "TestImpalaError.py", line 5, in <module>
    user='ldaptest', password='xxxx')
  File "/usr/local/lib/python2.7/site-packages/impala/dbapi.py", line 147, in connect
    auth_mechanism=auth_mechanism)
  File "/usr/local/lib/python2.7/site-packages/impala/hiveserver2.py", line 758, in connect
    transport.open()
  File "/usr/local/lib/python2.7/site-packages/thrift_sasl/__init__.py", line 72, in open
    message=("Could not start SASL: %s" % self.sasl.getError()))
TTransportException: Could not start SASL: Error in sasl_client_start (-4) SASL(-4): no mechanism available: No worthy mechs found

```

### Step 6: Java client for quering impala

```Java

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.Properties;
public class Hive2JdbcApp {
   public static void main(String[] args) {
       Connection conn = null;
       try{
           //org.apache.hive.jdbc.HiveDriver
           Class.forName("org.apache.hive.jdbc.HiveDriver");
           conn = DriverManager.getConnection("jdbc:hive2://10.10.100.51:21050/default;user=your_ldap_password;password=your_password");
           PreparedStatement pstm=conn.prepareStatement("show databases");
           ResultSet rs=pstm.executeQuery();
           while (rs.next()){
               System.out.println("databases："+rs.getString(1));
           }
       }catch (Exception e){
           e.printStackTrace();
       }
      }
}

```

## Good luck
