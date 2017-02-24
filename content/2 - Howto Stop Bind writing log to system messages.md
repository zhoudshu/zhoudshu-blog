Title: Howto Stop Bind writing log to system messages
Date: 2016-6-13 20:15
Tags: Bind,DNS,Logging,syslogd,messages
Category: Blog
Slug: Howto-Stop-Bind-writing-system-log-to-messages
Author: zhoudshu

[__Bind__](https://www.isc.org/downloads/bind/) is open source software that implements the Domain Name System (DNS) protocols for the Internet, Many Companies have used it. This article discusses the logging function of Bind. by default configuration, Bind writes logging to Linux system messages in /var/log/messages directory like:

     Jun 13 10:10:09 Test_Host named[19304]: success resolving 'ns4.servodns.com/A' (in 'servodns.com'?) after reducing the advertised EDNS UDP packet size to 512 octets
     Jun 13 10:10:09 Test_Host named[19304]: success resolving 'ns4.servodns.com/AAAA' (in 'servodns.com'?) after reducing the advertised EDNS UDP packet size to 512 octets
     Jun 13 10:10:10 Test_Host named[19304]: success resolving 'ns3.servodns.com/AAAA' (in 'servodns.com'?) after reducing the advertised EDNS UDP packet size to 512 octets
     Jun 13 10:10:10 Test_Host named[19304]: error (network unreachable) resolving 'www.research-results.de/A/IN': 2001:8d8:fe:53:0:d9a0:5090:100#53
     Jun 13 10:10:10 Test_Host named[19304]: adb: grow_names to 2039 starting
     Jun 13 10:10:10 Test_Host named[19304]: adb: grow_names finished

Sometimes, This default logging affectes the performance of bind, So We must find one method to close the logging. I looked at the document of bind, we can close it by configuring the following lines in named.conf
       
      category default { null; };

the whole logging configuration is follow:
     
      logging {
	       category default { null; };

	       channel "general" {
			file "log/general.log" versions 10 size 2000m;
			severity info;
			print-time      yes;
			print-category  yes;
			print-severity  yes;
	       };

	       category general {
			general;
	       };

	       channel "client" {
			file "log/client.log" versions 10 size 2000m;
			severity info;
			print-time      yes;
			print-category  yes;
			print-severity  yes;
	       };

	       category client{
			client;
	       };

	       channel "queries" {
			file "log/queries.log" versions 10 size 2000m;
			severity info;
			print-time      yes;
			print-category  yes;
			print-severity  yes;
	       };

	       category queries {
			queries;
	       };

        };

