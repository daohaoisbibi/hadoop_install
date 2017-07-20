# coding:utf-8

ZOO_CFG = """
# The number of milliseconds of each tick
tickTime=2000
# The number of ticks that the initial
# synchronization phase can take
initLimit=10
# The number of ticks that can pass between
# sending a request and getting an acknowledgement
syncLimit=5
# the directory where the snapshot is stored.
# do not use /tmp for storage, /tmp here is just
# example sakes.
dataDir=/home/USER/zookeeper-3.4.9/dataDir
# the port at which the clients will connect
clientPort=2181
# the maximum number of client connections.
# increase this if you need to handle more clients
#maxClientCnxns=60
#
# Be sure to read the maintenance section of the
# administrator guide before turning on autopurge.
#
# http://zookeeper.apache.org/doc/current/zookeeperAdmin.html#sc_maintenance
#
# The number of snapshots to retain in dataDir
#autopurge.snapRetainCount=3
# Purge task interval in hours
# Set to "0" to disable auto purge feature
#autopurge.purgeInterval=1
ZOOKEEPERS
"""
HDFS_SITE = """
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--
       Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->

<!-- Put site-specific property overrides in this file. -->

<configuration>
    <property>
    <name>dfs.datanode.data.dir</name>
    <value>/data1</value>
    </property>
    <property>
	<name>dfs.namenode.name.dir</name>
	<value>/name1</value>
    </property>
    <property>
        <name>dfs.block.access.token.enable</name>
        <value>true</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir.perm</name>
        <value>700</value>
    </property>
    <property>
        <name>dfs.namenode.keytab.file</name>
        <value>KEYTAB_PATH</value>
    </property>
 <property>
        <name>dfs.secondary.namenode.keytab.file</name>
        <value>KEYTAB_PATH</value>
    </property>
    <property>
        <name>dfs.namenode.kerberos.principal</name>
        <value>hadoop/_HOST@MLOGCN.INN</value>
    </property>
    <property>
        <name>dfs.namenode.kerberos.internal.spnego.principal</name>
        <value>HTTP/_HOST@MLOGCN.INN</value>
    </property>
    <property>
        <name>dfs.secondary.namenode.kerberos.internal.spnego.principal</name>
        <value>HTTP/_HOST@MLOGCN.INN</value>
    </property>

    <property>
        <name>dfs.datanode.address</name>
        <value>0.0.0.0:1004</value>
    </property>
    <property>
        <name>dfs.datanode.http.address</name>
        <value>0.0.0.0:1006</value>
    </property>
    <property>
        <name>dfs.datanode.keytab.file</name>
        <value>KEYTAB_PATH</value>
    </property>
    <property>
        <name>dfs.datanode.kerberos.principal</name>
        <value>hadoop/_HOST@MLOGCN.INN</value>
    </property>
    <property>
        <name>dfs.webhdfs.enable</name>
        <value>true</value>
    </property>
    <property>
        <name>dfs.web.authentication.kerberos.principal</name>
        <value>HTTP/_HOST@MLOGCN.INN</value>
    </property>
    <property>
        <name>dfs.web.authentication.kerberos.keytab</name>
        <value>KEYTAB_PATH</value>
    </property>
    <property>
        <name>dfs.namenode.acls.enabled</name>
        <value>true</value>
    </property>
</configuration>
"""

CORE_SITE = """
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->

<!-- Put site-specific property overrides in this file. -->

<configuration>
	<property>
                <name>fs.defaultFS</name>
                <value>hdfs://NAMENODE:9000</value>
        </property>
	<property>
	         <name>io.file.buffer.size</name>
       		 <value>131072</value>
       </property>
	   <property>
                <name>hadoop.tmp.dir</name>
                <value>TMP_DIR</value>
        </property>
	<property>
        	<name>hadoop.security.authentication</name>
        	<value>kerberos</value>
    	</property>
    	<property>
        	<name>hadoop.security.authorization</name>
        	<value>true</value>
    	</property>
	<property>
    		<name>hadoop.security.auth_to_local</name>
    		<value>
		RULE:[2:$1@$0](hadoop@.*MLOGCN.INN)s/.*/hadoop/
    		DEFAULT
		</value>
    		<description>Maps kerberos principals to local user names</description>
	</property>
        <property>
                <name>hadoop.proxyuser.hadoop.groups</name>
                <value>*</value>
	</property>
	<property>
		<name>hadoop.proxyuser.hadoop.hosts</name>
		<value>*</value>
	</property>
        <property>
                <name>hadoop.proxyuser.HTTP.groups</name>
                <value>*</value>
        </property>
        <property>
                <name>hadoop.proxyuser.HTTP.hosts</name>
                <value>*</value>
        </property>
	<property>
		<name>hadoop.proxyuser.hive.groups</name>
		<value>*</value>
	</property>
	<property>
                <name>hadoop.proxyuser.hive.hosts</name>
                <value>*</value>
        </property>
	 <property>
                <name>hadoop.proxyuser.yarn.groups</name>
                <value>*</value>
        </property>
	<property>
                <name>hadoop.proxyuser.yarn.hosts</name>
                <value>*</value>
        </property>
	<property>
                <name>hadoop.proxyuser.oozie.groups</name>
                <value>*</value>
        </property>
        <property>
                <name>hadoop.proxyuser.oozie.hosts</name>
                <value>*</value>
        </property>

	<!-- LDAP Configuration -->
	<property>
        	<name>hadoop.security.group.mapping</name>
        	<value>org.apache.hadoop.security.LdapGroupsMapping</value>
    	</property>
    	<property>
        	<name>hadoop.security.group.mapping.ldap.url</name>
        	<value>LDAP_URI</value>
    	</property>
    	<property>
        	<name>hadoop.security.group.mapping.ldap.bind.user</name>
        	<value>cn=admin,dc=mlogcn,dc=inn</value>
    	</property>
    	<property>
        	<name>hadoop.security.group.mapping.ldap.bind.password</name>
        	<value>LDAP_PWD</value>
    	</property>
    	<property>
        	<name>hadoop.security.group.mapping.ldap.base</name>
        	<value>dc=mlogcn,dc=inn</value>
    	</property>
    	<property>
        	<name>hadoop.security.group.mapping.ldap.search.filter.user</name>
        	<value>(&amp;(objectClass=person)(sn={0}))</value>
    	</property>
    	<property>
        	<name>hadoop.security.group.mapping.ldap.search.filter.group</name>
        	<value>(objectClass=groupOfNames)</value>
    	</property>
    	<property>
        	<name>hadoop.security.group.mapping.ldap.search.attr.member</name>
        	<value>member</value>
    	</property>
    	<property>
        	<name>hadoop.security.group.mapping.ldap.search.attr.group.name</name>
        	<value>cn</value>
    	</property>
<!--	<property>
   		<name>ipc.client.connect.max.retries</name>
   		<value>100</value>
   		<description>Indicates the number of retries a client will make to establish
       		a server connection.
   		</description>
 	</property>
 	<property>
   		<name>ipc.client.connect.retry.interval</name>
   		<value>10000</value>
   		<description>Indicates the number of milliseconds a client will wait for
  		before retrying to establish a server connection.
   		</description>
 	</property>-->
</configuration>

"""

MAPRED_SITE = """
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->

<!-- Put site-specific property overrides in this file. -->

<configuration>
  <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
<property>
  <name>mapreduce.jobhistory.keytab</name>
  <value>KEYTAB_PATH</value>
</property>
<property>
  <name>mapreduce.jobhistory.principal</name>
  <value>hadoop/_HOST@MLOGCN.INN</value>
</property>
  <property>
     <name>mapreduce.cluster.acls.enabled</name>
     <value>true</value>
  </property>
<property>
  <name>yarn.app.mapreduce.am.staging-dir</name>
  <value>/user</value>
</property>
</configuration>
"""
YARN_SITE = """
<?xml version="1.0"?>
<!--
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License. See accompanying LICENSE file.
-->
<configuration>
    <property>
       <name>yarn.resourcemanager.hostname</name>
       <value>NAMENODE</value>
    </property>
    <property>
	<name>yarn.resourcemanager.address</name>
        <value>NAMENODE:8032</value>
    </property>
    <property>
	<name>yarn.resourcemanager.resource-tracker.address</name>
	<value>NAMENODE:8031</value>
    </property>
    <property>
       <name>yarn.resourcemanager.zk-address</name>
       <value>ZOOKEEPER_URI</value>
    </property>
    <property>
       <name>yarn.nodemanager.aux-services</name>
       <value>mapreduce_shuffle</value>
    </property>

 <property>
    <name>yarn.nodemanager.pmem-check-enabled</name>
    <value>false</value>
</property>

<property>
    <name>yarn.nodemanager.vmem-check-enabled</name>
    <value>false</value>
</property>
<property>
        <name>yarn.resourcemanager.keytab</name>
        <value>KEYTAB_PATH</value>
</property>
<property>
        <name>yarn.resourcemanager.principal</name>
        <value>hadoop/_HOST@MLOGCN.INN</value>
</property>
<property>
        <name>yarn.nodemanager.keytab</name>
        <value>KEYTAB_PATH</value>
</property>
<property>
        <name>yarn.nodemanager.principal</name>
        <value>hadoop/_HOST@MLOGCN.INN</value>
</property>
<property>
  <name>yarn.resourcemanager.webapp.address</name>
 <value>NAMENODE:8088</value>
</property>
<property>
  <name>yarn.nodemanager.resource.memory-mb</name>
 <value>32768</value>
</property>
<property>
 <name>yarn.scheduler.maximum-allocation-mb</name>
 <value>16384</value>
</property>
</configuration>
"""

HIVE_SITE = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>javax.jdo.option.ConnectionURL</name>
        <value>jdbc:mysql://MYSQL_URI:3306/metastore?createDatabaseIfNotExist=true</value>
        <description>the URL of the MySQL database</description>
    </property>

    <property>
        <name>javax.jdo.option.ConnectionDriverName</name>
        <value>com.mysql.jdbc.Driver</value>
        <description>Driver class name for a JDBC metastore</description>
    </property>

    <property>
        <name>javax.jdo.option.ConnectionUserName</name>
        <value>hadoop</value>
    </property>

    <property>
        <name>javax.jdo.option.ConnectionPassword</name>
        <value>hadoop</value>
    </property>

    <property>
        <name>hive.metastore.warehouse.dir</name>
        <value>/hive/warehouse</value>
    </property>

    <property>
        <name>hive.exec.scratchdir</name>
        <value>/hive/tmp</value>
    </property>

    <property>
        <name>hive.querylog.location</name>
        <value>/hive/log</value>
    </property>

    <property>
        <name>hive.server2.enable.doAs</name>
        <value>true</value>
    </property>

    <property>
        <name>hive.server2.authentication</name>
        <value>KERBEROS</value>
    </property>

    <property>
        <name>hive.server2.authentication.kerberos.principal</name>
        <value>hadoop/_HOST@MLOGCN.INN</value>
    </property>

    <property>
        <name>hive.server2.authentication.kerberos.keytab</name>
        <value>KEYTAB_PATH</value>
    </property>

    <property>
        <name>hive.metastore.uris</name>
        <value>METASTORE_URI</value>
    </property>

    <property>
        <name>hive.metastore.sasl.enabled</name>
        <value>true</value>
    </property>

    <property>
        <name>hive.metastore.kerberos.keytab.file</name>
        <value>KEYTAB_PATH</value>
    </property>

    <property>
        <name>hive.metastore.kerberos.principal</name>
        <value>hadoop/_HOST@MLOGCN.INN</value>
    </property>


    <!-- 2017.3.31 Auth -->
    <property>
        <name>hive.metastore.authorization.storage.checks</name>
        <value>true</value>
    </property>
    <property>
        <name>hive.metastore.execute.setugi</name>
        <value>false</value>
    </property>

    <property>
        <name>hive.security.authorization.enabled</name>
        <value>true</value>
    </property>

    <property>
        <name>hive.security.authorization.createtable.owner.grants</name>
        <value>ALL</value>
    </property>

    <property>
        <name>hive.aux.jars.path</name>
        <value>file:///home/hadoop/apache-hive-1.2.1-bin/hive_aux.jar</value>
    </property>

    <property>
	<name>hive.semantic.analyzer.hook</name>
        <value>com.mlog.SuperHiveUser</value>
    </property>
</configuration>
"""

HBASE_ENV = """
#
#/**
# * Licensed to the Apache Software Foundation (ASF) under one
# * or more contributor license agreements.  See the NOTICE file
# * distributed with this work for additional information
# * regarding copyright ownership.  The ASF licenses this file
# * to you under the Apache License, Version 2.0 (the
# * "License"); you may not use this file except in compliance
# * with the License.  You may obtain a copy of the License at
# *
# *     http://www.apache.org/licenses/LICENSE-2.0
# *
# * Unless required by applicable law or agreed to in writing, software
# * distributed under the License is distributed on an "AS IS" BASIS,
# * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# * See the License for the specific language governing permissions and
# * limitations under the License.
# */

# Set environment variables here.

# This script sets variables multiple times over the course of starting an hbase process,
# so try to keep things idempotent unless you want to take an even deeper look
# into the startup scripts (bin/hbase, etc.)

# The java implementation to use.  Java 1.7+ required.
export JAVA_HOME=/usr/local/jdk1.8.0_121

# Extra Java CLASSPATH elements.  Optional.
# export HBASE_CLASSPATH=

# The maximum amount of heap to use. Default is left to JVM default.
# export HBASE_HEAPSIZE=1G

# Uncomment below if you intend to use off heap cache. For example, to allocate 8G of
# offheap, set the value to "8G".
# export HBASE_OFFHEAPSIZE=1G

# Extra Java runtime options.
# Below are what we set by default.  May only work with SUN JVM.
# For more on why as well as other possible settings,
# see http://wiki.apache.org/hadoop/PerformanceTuning

export HBASE_OPTS="-XX:+UseConcMarkSweepGC"

# Configure PermSize. Only needed in JDK7. You can safely remove it for JDK8+

# Uncomment one of the below three options to enable java garbage collection logging for the server-side processes.

# This enables basic gc logging to the .out file.
# export SERVER_GC_OPTS="-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps"

# This enables basic gc logging to its own file.
# If FILE-PATH is not replaced, the log file(.gc) would still be generated in the HBASE_LOG_DIR .
# export SERVER_GC_OPTS="-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xloggc:<FILE-PATH>"

# This enables basic GC logging to its own file with automatic log rolling. Only applies to jdk 1.6.0_34+ and 1.7.0_2+.
# If FILE-PATH is not replaced, the log file(.gc) would still be generated in the HBASE_LOG_DIR .
# export SERVER_GC_OPTS="-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xloggc:<FILE-PATH> -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=1 -XX:GCLogFileSize=512M"

# Uncomment one of the below three options to enable java garbage collection logging for the client processes.

# This enables basic gc logging to the .out file.
# export CLIENT_GC_OPTS="-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps"

# This enables basic gc logging to its own file.
# If FILE-PATH is not replaced, the log file(.gc) would still be generated in the HBASE_LOG_DIR .
# export CLIENT_GC_OPTS="-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xloggc:<FILE-PATH>"

# This enables basic GC logging to its own file with automatic log rolling. Only applies to jdk 1.6.0_34+ and 1.7.0_2+.
# If FILE-PATH is not replaced, the log file(.gc) would still be generated in the HBASE_LOG_DIR .
# export CLIENT_GC_OPTS="-verbose:gc -XX:+PrintGCDetails -XX:+PrintGCDateStamps -Xloggc:<FILE-PATH> -XX:+UseGCLogFileRotation -XX:NumberOfGCLogFiles=1 -XX:GCLogFileSize=512M"

# See the package documentation for org.apache.hadoop.hbase.io.hfile for other configurations
# needed setting up off-heap block caching.

# Uncomment and adjust to enable JMX exporting
# See jmxremote.password and jmxremote.access in $JRE_HOME/lib/management to configure remote password access.
# More details at: http://java.sun.com/javase/6/docs/technotes/guides/management/agent.html
# NOTE: HBase provides an alternative JMX implementation to fix the random ports issue, please see JMX
# section in HBase Reference Guide for instructions.

# export HBASE_JMX_BASE="-Dcom.sun.management.jmxremote.ssl=false -Dcom.sun.management.jmxremote.authenticate=false"
# export HBASE_MASTER_OPTS="$HBASE_MASTER_OPTS $HBASE_JMX_BASE -Dcom.sun.management.jmxremote.port=10101"
# export HBASE_REGIONSERVER_OPTS="$HBASE_REGIONSERVER_OPTS $HBASE_JMX_BASE -Dcom.sun.management.jmxremote.port=10102"
# export HBASE_THRIFT_OPTS="$HBASE_THRIFT_OPTS $HBASE_JMX_BASE -Dcom.sun.management.jmxremote.port=10103"
# export HBASE_ZOOKEEPER_OPTS="$HBASE_ZOOKEEPER_OPTS $HBASE_JMX_BASE -Dcom.sun.management.jmxremote.port=10104"
# export HBASE_REST_OPTS="$HBASE_REST_OPTS $HBASE_JMX_BASE -Dcom.sun.management.jmxremote.port=10105"

# File naming hosts on which HRegionServers will run.  $HBASE_HOME/conf/regionservers by default.
# export HBASE_REGIONSERVERS=${HBASE_HOME}/conf/regionservers

# Uncomment and adjust to keep all the Region Server pages mapped to be memory resident
#HBASE_REGIONSERVER_MLOCK=true
#HBASE_REGIONSERVER_UID="hbase"

# File naming hosts on which backup HMaster will run.  $HBASE_HOME/conf/backup-masters by default.
# export HBASE_BACKUP_MASTERS=${HBASE_HOME}/conf/backup-masters

# Extra ssh options.  Empty by default.
# export HBASE_SSH_OPTS="-o ConnectTimeout=1 -o SendEnv=HBASE_CONF_DIR"

# Where log files are stored.  $HBASE_HOME/logs by default.
# export HBASE_LOG_DIR=${HBASE_HOME}/logs

# Enable remote JDWP debugging of major HBase processes. Meant for Core Developers
# export HBASE_MASTER_OPTS="$HBASE_MASTER_OPTS -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=8070"
# export HBASE_REGIONSERVER_OPTS="$HBASE_REGIONSERVER_OPTS -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=8071"
# export HBASE_THRIFT_OPTS="$HBASE_THRIFT_OPTS -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=8072"
# export HBASE_ZOOKEEPER_OPTS="$HBASE_ZOOKEEPER_OPTS -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=8073"

# A string representing this instance of hbase. $USER by default.
# export HBASE_IDENT_STRING=$USER

# The scheduling priority for daemon processes.  See 'man nice'.
# export HBASE_NICENESS=10

# The directory where pid files are stored. /tmp by default.
# export HBASE_PID_DIR=/var/hadoop/pids

# Seconds to sleep between slave commands.  Unset by default.  This
# can be useful in large clusters, where, e.g., slave rsyncs can
# otherwise arrive faster than the master can service them.
# export HBASE_SLAVE_SLEEP=0.1

# Tell HBase whether it should manage it's own instance of Zookeeper or not.
export HBASE_MANAGES_ZK=false

# The default log rolling policy is RFA, where the log file is rolled as per the size defined for the
# RFA appender. Please refer to the log4j.properties file to see more details on this appender.
# In case one needs to do log rolling on a date change, one should set the environment property
# HBASE_ROOT_LOGGER to "<DESIRED_LOG LEVEL>,DRFA".
# For example:
# HBASE_ROOT_LOGGER=INFO,DRFA
# The reason for changing default to RFA is to avoid the boundary case of filling out disk space as
# DRFA doesn't put any cap on the log size. Please refer to HBase-5655 for more context.


export HADOOP_HOME=/home/USER/hadoop-2.7.3

export HBASE_CLASSPATH_PREFIX=/home/USER/hadoop-2.7.3/share/hadoop/common/hadoop-common-2.7.3.jar:/home/USER/hadoop-2.7.3/share/hadoop/hdfs/hadoop-hdfs-2.7.3.jar
"""

HBASE_SITE = """
<?xml version="1.0"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<!--
/**
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
-->
<configuration>
	<property>
		<name>hbase.rootdir</name>
		<value>hdfs://NAMENODE:9000/hbase</value>
	</property>
	<property>
		<name>hbase.cluster.distributed</name>
		<value>true</value>
	</property>
	<property>
		<name>hbase.zookeeper.quorum</name>
		<value>ZOOKEEPER_URI</value>
	</property>
<property>
    <name>hbase.zookeeper.property.dataDir</name>
    <value>HBASE_ZK_DIR</value>
  </property>
	<property>
		<name>hbase.tmp.dir</name>
		<value>HBASE_TMP_DIR</value>
	</property>
	<property>
    		<name>hbase.security.authentication</name>
    		<value>kerberos</value>
	</property>
    	<property>
        	<name>hbase.security.authorization</name>
        	<value>true</value>
      	</property>
 	<property>
  		<name>hbase.coprocessor.master.classes</name>
  		<value>org.apache.hadoop.hbase.security.access.AccessController</value>
 	</property>
      	<property>
      		<name>hbase.coprocessor.region.classes</name>
        	<value>org.apache.hadoop.hbase.security.token.TokenProvider</value>
      	</property>
	 <property>
  		<name>hbase.rpc.engine</name>
  		<value>org.apache.hadoop.hbase.ipc.SecureRpcEngine</value>
 	</property>
	<property>
		<name>hbase.regionserver.kerberos.principal</name>
  		<value>hadoop/_HOST@MLOGCN.INN</value>
	</property>
	<property>
  		<name>hbase.regionserver.keytab.file</name>
  		<value>KEYTAB_PATH</value>
	</property>
	<property>
  		<name>hbase.master.kerberos.principal</name>
  		<value>hadoop/_HOST@MLOGCN.INN</value>
	</property>
	<property>
		<name>hbase.master.keytab.file</name>
		<value>KEYTAB_PATH</value>
	</property>
	<property>
  		<name>hbase.rest.authentication.type</name>
  		<value>kerberos</value>
 	</property>
	<property>
                <name>hbase.rest.authentication.kerberos.principal</name>
                <value>hadoop/_HOST@MLOGCN.INN</value>
        </property>
        <property>
                <name>hbase.rest.authentication.keytab.file</name>
                <value>KEYTAB_PATH</value>
        </property>
</configuration>
"""

COORDINATOR = """
coordinator=true
node-scheduler.include-coordinator=false
http-server.http.port=7670
query.max-memory=16GB
query.max-memory-per-node=4GB
discovery-server.enabled=true
discovery.uri=http://CONNRDINATOR:7670
"""
WORKER = """
coordinator=false
http-server.http.port=7670
query.max-memory=16GB
query.max-memory-per-node=2GB
discovery.uri=http://CONNRDINATOR:7670
"""
PRESTO_NODE = """
node.environment=prod
node.id=NODE_ID
node.data-dir=/home/hadoop/presto/data
"""

SPARK_ENV = """
export JAVA_HOME=/usr/local/jdk1.8.0_121
export HADOOP_HOME=/home/USER/hadoop-2.7.3
export HADOOP_CONF_DIR=/home/USER/hadoop-2.7.3/etc/hadoop
#export HIVE_HOME=/home/USER/apache-hive-1.2.1-bin
export SPARK_DAEMON_JAVA_OPTS="-Dspark.deploy.recoveryMode=ZOOKEEPER -Dspark.deploy.zookeeper.url=ZOOKEEPER_URI -Dspark.deploy.zookeeper.dir=/spark"
export SPARK_YARN_USER_ENV="CLASSPATH=/home/USER/hadoop-2.7.3/etc/hadoop"
"""
SPARK_CONF = """
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Default system properties included when running spark-submit.
# This is useful for setting default environmental settings.

# Example:
# spark.master                     spark://master:7077
# spark.eventLog.enabled           true
# spark.eventLog.dir               hdfs://namenode:8021/directory
# spark.serializer                 org.apache.spark.serializer.KryoSerializer
# spark.driver.memory              5g
# spark.executor.extraJavaOptions  -XX:+PrintGCDetails -Dkey=value -Dnumbers="one two three"

# authentication
spark.authenticate                              true
# spark.authenticate.enableSaslEncryption               true

# serializer
spark.serializer                                org.apache.spark.serializer.KryoSerializer

# eventLog
# spark.eventLog.enabled                        true
# spark.eventLog.compress                       true
# spark.eventLog.dir                            hdfs://ns/tmp/spark-eventLog
# spark.yarn.historyServer.address              0.0.0.0:18080

spark.sql.warehouse.dir                         hdfs://NAMENODE:9000/hive/warehouse

# SciSpark
spark.driver.extraClassPath                     /home/USER/spark-2.1.0-bin-hadoop2.7/jars/SciSpark.jar:/home/USER/spark-2.1.0-bin-hadoop2.7/jars/mysql-connector-java-5.1.38.jar
spark.executor.extraClassPath                   /home/USER/spark-2.1.0-bin-hadoop2.7/jars/SciSpark.jar:/home/USER/spark-2.1.0-bin-hadoop2.7/jars/mysql-connector-java-5.1.38.jar
"""

AZKABAN_SERVER = """
azkaban.color=#FF3601
azkaban.default.servlet.path=/index
web.resource.dir=web/
default.timezone.id=Asia/Shanghai
database.type=mysql
mysql.port=3306
mysql.host=MYSQL_URI
mysql.database=azkaban
mysql.user=azkaban
mysql.password=azkaban
mysql.numconnections=50
jetty.use.ssl=false
jetty.maxThreads=200
jetty.port=8081
user.manager.class=azkaban.user.XmlUserManager
user.manager.xml.file=conf/azkaban-users.xml
azkaban.use.multiple.executors=true
azkaban.executorselector.filters=StaticRemainingFlowSize,MinimumFreeMemory,CpuStatus
azkaban.executorselector.comparator.NumberOfAssignedFlowComparator=1
azkaban.executorselector.comparator.Memory=1
azkaban.executorselector.comparator.LastDispatched=1
azkaban.executorselector.comparator.CpuUsage=1
"""

AZKABAN_EXEC = """
default.timezone.id=Asia/Shanghai
database.type=mysql
mysql.port=3306
mysql.host=MYSQL_URI
mysql.database=azkaban
mysql.user=azkaban
mysql.password=azkaban
mysql.numconnections=50
executor.maxThreads=50
executor.port=12321
executor.flow.threads=30
azkaban.native.lib=nativelib
azkaban.webserver.url=http://AZKABAN_URI:8081
azkaban.jobtype.plugin.dir=plugins/jobtypes
"""

AZKABAN_COMMON_PRIVATE = """
Execute.as.user=false
jvm.args=-Xms512m -Xmx2048m
azkaban.native.lib=/home/USER/azkaban/azkaban-exec-server-3.15.0/nativelib
hadoop.security.manager.class=azkaban.security.HadoopSecurityManager_H_2_0
azkaban.should.proxy=false
proxy.user=hadoop/AZKABAN_URI@MLOGCN.INN
proxy.keytab.location=/home/USER/.keys/hadoop.keytab
hadoop.home=/home/USER/hadoop-2.7.3
spark.home=/home/USER/spark-2.1.0-bin-hadoop2.7
hadoop.share=${hadoop.home}/share/hadoop
jobtype.global.classpath=${hadoop.home}/etc/hadoop,${hadoop.share}/common/hadoop-common-2.7.3.jar,${hadoop.share}/hdfs/hadoop-hdfs-2.7.3.jar,${hadoop.share}/yarn/lib/protobuf-java-2.5.0.jar,${hadoop.share}/yarn/hadoop-yarn-common-2.7.3.jar,${hadoop.share}/yarn/hadoop-yarn-api-2.7.3.jar,${hadoop.share}/yarn/hadoop-yarn-server-common-2.7.3.jar,${hadoop.share}/yarn/hadoop-yarn-client-2.7.3.jar
hadoop.classpath=${hadoop.home}/etc/hadoop/conf
spark.jar=${spark.home}/jars
spark.classpath=${spark.jar}/spark-core_2.11-2.1.0.jar,${spark.jar}/spark-yarn_2.11-2.1.0.jar,${spark.jar}/spark-network-common_2.11-2.1.0.jar,${spark.jar}/spark-network-shuffle_2.11-2.1.0.jar,${spark.jar}/spark-launcher_2.11-2.1.0.jar,${spark.jar}/spark-sql_2.11-2.1.0.jar,${spark.jar}/spark-hive_2.11-2.1.0.jar,${spark.jar}/spark-unsafe_2.11-2.1.0.jar,${spark.jar}/spark-hive-thriftserver_2.11-2.1.0.jar
"""

MY_CONF = """
# For advice on how to change settings please see
# http://dev.mysql.com/doc/refman/5.7/en/server-configuration-defaults.html

[mysqld]
#
# Remove leading # and set to the amount of RAM for the most important data
# cache in MySQL. Start at 70% of total RAM for dedicated server, else 10%.
# innodb_buffer_pool_size = 128M
#
# Remove leading # to turn on a very important data integrity option: logging
# changes to the binary log between backups.
# log_bin
#
# Remove leading # to set options mainly useful for reporting servers.
# The server defaults are faster for transactions and fast SELECTs.
# Adjust sizes as needed, experiment to find the optimal values.
# join_buffer_size = 128M
# sort_buffer_size = 2M
# read_rnd_buffer_size = 2M
datadir=/var/lib/mysql
socket=/var/lib/mysql/mysql.sock

# Disabling symbolic-links is recommended to prevent assorted security risks
symbolic-links=0
max_allowed_packet=50m
log-error=/var/log/mysqld.log
pid-file=/var/run/mysqld/mysqld.pid
"""
