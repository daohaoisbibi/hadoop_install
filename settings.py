import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RESOURCES_DIR = os.path.join(BASE_DIR, "resources")

TMP_DIR = os.path.join(BASE_DIR, "tmp")

CONFIG_FILE = os.path.join(BASE_DIR, "config.json")

USER = "hadoop"

PASSWORD = "gavial!@#"

LDAP_PWD = "gavial"

KEYTAB_PATH = "/home/{0}/.keys/hadoop.keytab".format(USER)

HADOOP_TMP_DIR = "/home/{0}/hadoop-2.7.3/tmp".format(USER)

HBASE_TMP_DIR = "/home/{0}/hbase-1.2.4/tmp".format(USER)

HBASE_ZK_DIR = "/home/{0}/hbase-1.2.4/zkdata".format(USER)

ZOOKEEPER_TMP_DIR = "/home/{0}/zookeeper-3.4.9/dataDir".format(USER)

ZK_DEFAULT_CONF_PATH = "/home/{0}/zookeeper-3.4.9/conf/zoo.cfg".format(USER)

SPARK_DEFAULT_CONF_PATH = "/home/{0}/spark-2.1.0-bin-hadoop2.7/conf/".format(USER)

HADOOP_DEFAULT_CONF_PATH = "/home/{0}/hadoop-2.7.3/etc/hadoop".format(USER)

HIVE_DEFAULT_PATH = "/home/{0}/apache-hive-1.2.1-bin".format(USER)

HBASE_DEFAULT_CONF_PATH = "/home/{0}/hbase-1.2.4/conf".format(USER)

PRESTO_DEFAULT_CONF_PATH = "/home/{0}/presto/presto-server-0.170/etc".format(USER)

REDIS_DEFAULT_PATH = "/home/{0}/redis-3.2.9".format(USER)

AZKABAN_WEB_DEFAULT_PATH = "/home/{0}/azkaban/azkaban-web-server-3.15.0".format(USER)
AZKABAN_EXEC_DEFAULT_PATH = "/home/{0}/azkaban/azkaban-exec-server-3.15.0".format(USER)
