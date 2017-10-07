MongoDB Enterprise contains the following configuration files to
support SNMP:

1) MONGOD-MIB.txt

The management information base (MIB) file that defines MongoDB’s
SNMP output.

2) mongod.conf.subagent

The configuration file to run mongod as the SNMP subagent. This
file sets SNMP run-time configuration options, including the AgentX
socket to connect to the SNMP master.

3) mongod.conf.master

The configuration file to run mongod as the SNMP master. This file
sets SNMP run-time configuration options.

For more information, see: 
1) http://docs.mongodb.org/master/tutorial/monitor-with-snmp-on-windows/
2) http://docs.mongodb.org/master/tutorial/monitor-with-snmp/
3) http://docs.mongodb.org/master/tutorial/troubleshoot-snmp/
