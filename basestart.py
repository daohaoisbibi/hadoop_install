# encoding: utf-8
from settings import *
from linuxclient import LinuxClient


def hadoop_start(info):
    ssh_client = LinuxClient(info["ip"], username=USER, password=PASSWORD, port=info["port"])
    root_ssh_client = LinuxClient(info["ip"], username=USER, password=PASSWORD, port=info["port"])

    cmd_set = (
        "cd /home/{0}/hadoop-2.7.3/bin/;./hdfs namenode -format".format(USER),
        "cd /home/{0}/hadoop-2.7.3/sbin/;./start-dfs.sh".format(USER),
        "cd /home/{0}/hadoop-2.7.3/sbin/;./start-yarn.sh".format(USER),
    )
    map(ssh_client.exec_shell_command, cmd_set)
    root_ssh_client.exec_shell_command("cd /home/{0}/hadoop-2.7.3/sbin/;./start-secure-dns.sh".format(USER))
    ssh_client.release()
    root_ssh_client.release()


def hbase_start(info):
    ssh_client = LinuxClient(info["ip"], username=USER, password=PASSWORD, port=info["port"])
    ssh_client.exec_shell_command("cd /home/{0}/hbase-1.2.4/bin;./start-hbase.sh".format(USER))
    ssh_client.release()


def hive_start(info):
    ssh_client = LinuxClient(info["ip"], username=USER, password=PASSWORD, port=info["port"])
    ssh_client.exec_shell_command("cd /home/{0}/apache-hive-1.2.1-bin;./bin/hive -service metastore &".format(USER))
    ssh_client.release()


def presto_start(info):
    ssh_client = LinuxClient(info["ip"], username=USER, password=PASSWORD, port=info["port"])
    ssh_client.exec_shell_command("cd /home/{0}/presto/presto-server-0.170/bin;./launcher start".format(USER))
    ssh_client.release()


def redis_start(info):
    pass


def zookeeper_start(info):
    ssh_client = LinuxClient(info["ip"], username=USER, password=PASSWORD, port=info["port"])
    ssh_client.exec_shell_command("cd /home/{0}/zookeeper-3.4.9/bin;./zkServer.sh start".format(USER))
    ssh_client.release()


def azkaban_start(info):
    ssh_client = LinuxClient(info["ip"], username=USER, password=PASSWORD, port=info["port"])
    ssh_client.exec_shell_command(
        "cd /home/{0}/azkaban/azkaban-exec-server-3.15.0;./bin/azkaban-exec-start.sh".format(USER))
    ssh_client.exec_shell_command(
        "cd /home/{0}/azkaban/azkaban-web-server-3.15.0;./bin/azkaban-web-start.sh".format(USER))
    ssh_client.release()


def kadmin_ldap_server_start(info):
    ssh_client = LinuxClient(info["ip"], username=USER, password=PASSWORD, port=info["port"])
    ssh_client.exec_shell_command("cd /home/{0}/kadmin_ldap_server;python app.py &".format(USER))
    ssh_client.release()
