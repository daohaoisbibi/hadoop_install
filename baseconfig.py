# coding:utf-8
import os
from settings import *
from defaultconfig import *
from ldapconfig import ETC_KRB5


def set_zoocfg(zookeepers):
    zoocfg = os.path.join(TMP_DIR, "zoo.cfg")
    with open(zoocfg, "w") as f:
        f.write(ZOO_CFG.replace("ZOOKEEPERS", "".join(
            ["\nserver.{0}={1}:2888:3888".format(zookeepers.index(host_name) + 1, host_name) for host_name in
             zookeepers])).replace("USER", USER))


def set_hdfs_site():
    hdfs_site = os.path.join(TMP_DIR, "hdfs-site.xml")
    with open(hdfs_site, "w") as f:
        f.write(HDFS_SITE.replace("KEYTAB_PATH", KEYTAB_PATH))


def set_core_site(ldap, namenode):
    core_site = os.path.join(TMP_DIR, "core-site.xml")
    with open(core_site, "w") as f:
        f.write(CORE_SITE.replace("NAMENODE", namenode)
                .replace("TMP_DIR", HADOOP_TMP_DIR)
                .replace("LDAP_URI", "ldap://{0}".format(ldap)).replace("LDAP_PWD", LDAP_PWD))


def set_mapred_site():
    mapred_site = os.path.join(TMP_DIR, "mapred-site.xml")
    with open(mapred_site, "w") as f:
        f.write(MAPRED_SITE.replace("KEYTAB_PATH", KEYTAB_PATH))


def set_yarn_site(zookeepers, namenode):
    yarn_site = os.path.join(TMP_DIR, "yarn-site.xml")
    with open(yarn_site, "w") as f:
        f.write(YARN_SITE.replace("KEYTAB_PATH", KEYTAB_PATH)
                .replace("NAMENODE", namenode)
                .replace("ZOOKEEPER_URI", ",".join(["{0}:2181".format(host_name) for host_name in zookeepers])))


def set_hbase_site(zookeepers, hmaster):
    hbase_site = os.path.join(TMP_DIR, "hbase-site.xml")
    with open(hbase_site, "w") as f:
        f.write(HBASE_SITE.replace("HBASE_TMP_DIR", HBASE_TMP_DIR)
                .replace("HBASE_ZK_DIR", HBASE_ZK_DIR)
                .replace("KEYTAB_PATH", KEYTAB_PATH)
                .replace("NAMENODE", hmaster)
                .replace("ZOOKEEPER_URI", ",".join(
            ["{0}:2181".format(host_name) for host_name in zookeepers])))


def set_hbase_env():
    hbase_env = os.path.join(TMP_DIR, "hbase-env.sh")
    with open(hbase_env, "w") as f:
        f.write(HBASE_ENV.replace("USER", USER))


def set_hive_site(mysql_uri, metastores):
    hive_site = os.path.join(TMP_DIR, "hive-site.xml")
    with open(hive_site, "w") as f:
        f.write(HIVE_SITE.replace("KEYTAB_PATH", KEYTAB_PATH)
                .replace("MYSQL_URI", mysql_uri)
                .replace("METASTORE_URI",
                         ",".join(["thrift://{0}:9083".format(host_name) for host_name in metastores])))


def set_spark_conf(namenode):
    spark_conf = os.path.join(TMP_DIR, "spark-defaults.conf")
    with open(spark_conf, "w") as f:
        f.write(SPARK_CONF.replace("NAMENODE", namenode).replace("USER", USER))


def set_spark_env(zookeepers):
    spark_env = os.path.join(TMP_DIR, "spark-env.sh")
    with open(spark_env, "w") as f:
        f.write(SPARK_ENV.replace("ZOOKEEPER_URI", ",".join(
            ["{0}:2181".format(host_name) for host_name in zookeepers])).replace("USER", USER))


def set_presto_node(node_id):
    node_pro = os.path.join(TMP_DIR, "node.properties")
    with open(node_pro, "w") as f:
        f.write(PRESTO_NODE.replace("NODE_ID", node_id))


def set_presto_config(coordinator, is_worker=True):
    config_pro = os.path.join(TMP_DIR, "config.properties")
    with open(config_pro, "w") as f:
        f.write(
            WORKER.replace("CONNRDINATOR", coordinator) if type else COORDINATOR.replace("CONNRDINATOR", coordinator))


def set_krb5_conf(ip):
    krb5 = os.path.join(TMP_DIR, "krb5.conf")
    with open(krb5, "w") as f:
        f.write(ETC_KRB5.replace("KDC_SERVER", ip))


def set_hadoop_slaves(datanodes):
    hadoop_slaves = os.path.join(TMP_DIR, "hadoop-slaves")
    with open(hadoop_slaves, "w") as f:
        f.writelines(["{0}\n".format(host_name) for host_name in datanodes])


def set_spark_slaves(sparks):
    spark_slaves = os.path.join(TMP_DIR, "spark-slaves")
    with open(spark_slaves, "w") as f:
        f.writelines(["{0}\n".format(host_name) for host_name in sparks])


def set_region_servers(region_servers):
    region_server = os.path.join(TMP_DIR, "regionservers")
    with open(region_server, "w") as f:
        f.writelines(["{0}\n".format(host_name) for host_name in region_servers])


def set_azkaban_server(mysql_uri):
    azkaban_server = os.path.join(TMP_DIR, "azkaban-web.properties")
    with open(azkaban_server, "w") as f:
        f.write(AZKABAN_SERVER.replace("MYSQL_URI", mysql_uri))


def set_azkaban_exec(mysql_uri, azkaban_uri):
    azkaban_exec = os.path.join(TMP_DIR, "azkaban-exec.properties")
    with open(azkaban_exec, "w") as f:
        f.write(AZKABAN_EXEC.replace("MYSQL_URI", mysql_uri).replace("AZKABAN_URI", azkaban_uri))


def set_common_pri(azkaban_uri):
    common_pri = os.path.join(TMP_DIR, "commonprivate.properties")
    with open(common_pri, "w") as f:
        f.write(AZKABAN_COMMON_PRIVATE.replace("USER", USER).replace("AZKABAN_URI", azkaban_uri))


def save_keytab(ssh_client, dict):
    user_keytab = 'kadmin.local -q "addprinc -pw \'gavial\' {0}"'
    list1 = map(lambda x: "hadoop/{0}".format(x), dict.keys())
    list2 = map(lambda x: "HTTP/{0}".format(x), dict.keys())
    users = ["hadoop", "hadoop/_HOST", "HTTP/_HOST", "root", "root/admin"]
    users.extend(list1)
    users.extend(list2)
    cmd_set = map(lambda x: user_keytab.format(x), users)
    cmd_set.append('kadmin.local -q "xst -k /root/hadoop.keytab {0}"'.format(" ".join(users)))
    map(ssh_client.exec_shell_command, cmd_set)
    ssh_client.transport_file2local(os.path.join(RESOURCES_DIR, ".keys/hadoop.keytab"), "/root/hadoop.keytab")
