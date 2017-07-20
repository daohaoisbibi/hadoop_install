# coding:utf-8
from __future__ import unicode_literals
import json, re
from baseinstall import *
from basestart import *
from baseconfig import *
from linuxclient import LinuxClient


def server_init(info):
    host_name = info["hostname"]
    ssh_client = LinuxClient(info["ip"], username="root", password=info["password"],
                             port=info["port"])
    no_secret(ssh_client, is_root=True)
    add_user(ssh_client)
    global etc_hosts, mysql_server, ldap_server, host_dict
    fix_host(ssh_client, host_name, etc_hosts)
    jdk(ssh_client)
    if mysql_server == host_name:
        mysql(ssh_client)
        ssh_client.release()
        ssh_client = LinuxClient(info["ip"], username="root", password=info["password"],
                                 port=info["port"])
        ssh_client.exec_shell_command("echo 'max_allowed_packet=50m' >> /etc/my.cnf")
        ssh_client.release()
        ssh_client = LinuxClient(info["ip"], username="root", password=info["password"],
                                 port=info["port"])
        ssh_client.exec_shell_command("systemctl start mysqld")
        create_database(ssh_client)
    if ldap_server == host_name:
        kdcldap(ssh_client)
        mlogcn_inn(ssh_client, info["ip"])
        pythonldap(ssh_client)
        save_keytab(ssh_client, host_dict)
    ssh_client.transport_file(os.path.join(TMP_DIR, "krb5.conf"), "/etc/krb5.conf")
    ssh_client.release()


def hadoopy_install(info):
    host_name = info["hostname"]
    ssh_client = LinuxClient(info["ip"], username=USER, password=PASSWORD, port=info["port"])
    no_secret(ssh_client)
    ssh_client.transport_dir(os.path.join(RESOURCES_DIR, ".keys/"), "/home/{0}/.keys".format(USER))
    global namenode, datanodes, hmaster, regionservers, spark_server, metastores
    global coordinator, workers, redis_server, zookeepers, azkaban_server, ldap_server
    if host_name == namenode or host_name in datanodes:
        hadoop(ssh_client)
    if host_name == hmaster or host_name in regionservers:
        hbase(ssh_client)
    if host_name == namenode or host_name in spark_server or host_name in metastores:
        hive(ssh_client)
        spark(ssh_client)
    if host_name == coordinator or host_name in workers:
        set_presto_config(coordinator, host_name == coordinator)
        set_presto_node("master" if host_name == coordinator else "worker-{0}".format(workers.index(host_name) + 1))
        presto(ssh_client)
    if host_name == redis_server:
        redis(ssh_client)
    if host_name in zookeepers:
        zookeeper(ssh_client, zookeepers.index(host_name) + 1)
    if host_name == azkaban_server:
        azkaban(ssh_client)
    if ldap_server == host_name:
        kadmin_ldap_server(ssh_client, ldap_server)
    ssh_client.release()


def start_services():
    global zookeepers, host_dict
    for item in zookeepers:
        zookeeper_start(host_dict.get(item))
    hadoop_start(host_dict.get(namenode))
    hbase_start(host_dict.get(hmaster))
    for item in metastores:
        hive_start(host_dict.get(item))
    presto_start(host_dict.get(coordinator))
    for item in workers:
        presto_start(host_dict.get(item))
    azkaban_start(host_dict.get(azkaban_server))
    kadmin_ldap_server_start(host_dict.get(ldap_server))
    redis_start(host_dict.get(redis_server))


def hadoopy_config():
    global zookeepers, namenode, hmaster, ldap_server, mysql_server, metastores, host_dict
    global datanodes, spark_server, regionservers, azkaban_server
    set_zoocfg(zookeepers)
    set_hdfs_site()
    set_core_site(host_dict.get(ldap_server)["ip"], namenode)
    set_mapred_site()
    set_mapred_site()
    set_yarn_site(zookeepers, namenode)
    set_hbase_site(zookeepers, hmaster)
    set_hbase_env()
    set_hive_site(mysql_server, metastores)
    set_spark_conf(namenode)
    set_spark_env(zookeepers)
    set_krb5_conf(host_dict.get(ldap_server)["ip"])
    set_hadoop_slaves(datanodes)
    set_spark_slaves(spark_server)
    set_region_servers(regionservers)
    set_azkaban_server(mysql_server)
    set_azkaban_exec(mysql_server, azkaban_server)
    set_common_pri(azkaban_server)


with open(CONFIG_FILE, "r") as f:
    jsonobj = json.load(f)
print(jsonobj["clusterName"])
hosts = jsonobj["hosts"]
etc_hosts = ["{0} {1}".format(info["ip"], info["hostname"]) for info in hosts]
zookeepers = jsonobj["zookeeper"]
host_dict = {info["hostname"]: info for info in hosts}
mysql_server = jsonobj["mysql"]
metastores = jsonobj["metastore"]
namenode = jsonobj["namenode"]
hmaster = jsonobj["hmaster"]
azkaban_server = jsonobj["azkaban"]
ldap_server = jsonobj["ldap"]
redis_server = jsonobj["redis"]
datanodes = jsonobj["datanode"]
regionservers = jsonobj["regionservers"]
coordinator = jsonobj["coordinator"]
workers = jsonobj["workers"]
spark_server = ["spark"]
# hadoopy_config()
# map(server_init, hosts)
# map(server_init, hosts)
map(hadoopy_install, hosts)


"""
paramiko-2.2.1-py2.py3-none-any.whl
pyasn1-0.2.3-py2.py3-none-any.whl  pyasn1>=0.1.7
bcrypt>=3.1.3
cryptography>=1.1
pynacl>=1.0.1
pycparser-2.18
cffi>=1.1 (from bcrypt>=3.1.3->paramiko)
six>=1.4.1 in /usr/lib/python2.7/dist-packages (from bcrypt>=3.1.3->paramiko)
asn1crypto>=0.21.0 (from cryptography>=1.1->paramiko)
enum34 (from cryptography>=1.1->paramiko)
ipaddress (from cryptography>=1.1->paramiko)
pycparser (from cffi>=1.1->bcrypt>=3.1.3->paramiko)
 idna>=2.1 (from cryptography>=1.1->paramiko)
"""