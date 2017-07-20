# encoding: utf-8
from settings import *
from ldapconfig import *
import re

RPM_IVH = "rpm -ivh {0}"

RPM_UVH = "rpm -Uvh {0}"


def no_secret(ssh_client, is_root=False):
    secret_dir = os.path.join(RESOURCES_DIR, '.ssh')
    remote_dir = "/root/.ssh" if is_root else "/home/{0}/.ssh".format(USER)
    ssh_client.transport_dir(secret_dir, remote_dir)
    if not is_root:
        ssh_client.exec_shell_command("chown -R {0}. {1}".format(USER, remote_dir), use_root=True)
    ssh_client.exec_shell_command("chmod 600 ~/.ssh/authorized_keys")
    print("no secret seccuss")


def add_user(ssh_client):
    salt = "gavial-ng"
    cmd = 'useradd -p `openssl passwd -1 -salt \"' + salt + '\" ' + PASSWORD + '` ' + USER
    ssh_client.exec_shell_command(cmd)

    cmd = "chmod u+w /etc/sudoers;echo '{0} ALL=(ALL) ALL' >> /etc/sudoers;chmod u-w /etc/sudoers".format(
        USER)
    ssh_client.exec_shell_command(cmd)

    print("add user seccuss")


def fix_host(ssh_client, hostname, hosts_list):
    cmd = "echo '{0}' > /etc/hostname;".format(hostname)
    ssh_client.exec_shell_command(cmd)

    cmd = ";".join(["echo '{0}' >> /etc/hosts".format(item) for item in hosts_list])
    ssh_client.exec_shell_command(cmd)
    print("fix host seccuss")


def jdk(ssh_client):
    jdk_path = os.path.join(RESOURCES_DIR, 'jdk1.8.0_121.tar.gz')
    ssh_client.transport_file(jdk_path, "/root/jdk1.8.0_121.tar.gz")
    cmd_set = ("tar zxf /root/jdk1.8.0_121.tar.gz",
               "mv /root/jdk1.8.0_121 /usr/local/jdk1.8.0_121",
               "echo 'export JAVA_HOME=/usr/local/jdk1.8.0_121' >> /etc/profile",
               "echo 'export PATH=$JAVA_HOME/bin:$JAVA_HOME/jre/bin:$PATH' >> /etc/profile",
               "source /etc/profile")
    map(ssh_client.exec_shell_command, cmd_set)
    print("install jdk seccuss")


def kdcldap(ssh_client):
    local_dir = os.path.join(RESOURCES_DIR, 'kdcldap')
    remote_dir = "/root/kdcldap"
    ssh_client.transport_dir(local_dir, remote_dir)
    cmd_set = (
        RPM_IVH.format(os.path.join(remote_dir, "openldap-server/libtool-ltdl-2.4.2-22.el7_3.x86_64.rpm")),
        RPM_UVH.format(os.path.join(remote_dir, "openldap-server/openldap-2.4.40-13.el7.x86_64.rpm")),
        RPM_IVH.format(os.path.join(remote_dir, "openldap-server/openldap-servers-2.4.40-13.el7.x86_64.rpm")),
        RPM_IVH.format(os.path.join(remote_dir, "openldap-clients/openldap-clients-2.4.40-13.el7.x86_64.rpm")),
        RPM_UVH.format(os.path.join(remote_dir, "krb5-server-ldap/krb5-libs-1.14.1-27.el7_3.x86_64.rpm")),
        RPM_IVH.format(os.path.join(remote_dir, "krb5-server-ldap/libkadm5-1.14.1-27.el7_3.x86_64.rpm")),
        RPM_IVH.format(os.path.join(remote_dir, "krb5-server-ldap/libevent-2.0.21-4.el7.x86_64.rpm")),
        RPM_IVH.format(os.path.join(remote_dir, "krb5-server-ldap/libverto-libevent-0.2.5-4.el7.x86_64.rpm")),
        RPM_IVH.format(os.path.join(remote_dir, "krb5-server-ldap/words-3.0-22.el7.noarch.rpm")),
        RPM_IVH.format(os.path.join(remote_dir, "krb5-server-ldap/krb5-server-1.14.1-27.el7_3.x86_64.rpm")),
        RPM_IVH.format(os.path.join(remote_dir, "krb5-server-ldap/krb5-server-ldap-1.14.1-27.el7_3.x86_64.rpm")),
    )
    map(ssh_client.exec_shell_command, cmd_set)


def mlogcn_inn(ssh_client, ip):
    local_dir = os.path.join(RESOURCES_DIR, 'ldap')
    remote_dir = "/root/ldap"
    ssh_client.transport_dir(local_dir, remote_dir)

    cmd_set = (
        "cp /usr/share/openldap-servers/DB_CONFIG.example /var/lib/ldap/DB_CONFIG",
        "chown -R ldap. /var/lib/ldap",
        "systemctl start slapd",
        "systemctl enable slapd",
        "systemctl status slapd"
    )
    map(ssh_client.exec_shell_command, cmd_set)
    stdin, stdout, stderr = ssh_client.ssh_client.exec_command("slappasswd", get_pty=True)
    stdin.write("gavial\n")
    stdin.flush()
    stdin.write("gavial\n")
    stdin.flush()
    ssha_key = stdout.readlines()[-1]
    chrootpw = os.path.join(TMP_DIR, "chrootpw.ldif")
    with open(chrootpw, "w") as f:
        f.write(CHROOTPW.replace("SSHA_KEY", ssha_key))
    ssh_client.transport_file(chrootpw, "/root/chrootpw.ldif")
    cmd_set = (
        "ldapadd -Y EXTERNAL -H ldapi:/// -f /root/chrootpw.ldif",
        "cp /usr/share/doc/krb5-server-ldap-1.14.1/kerberos.schema /etc/openldap/schema/",
        "mkdir /root/kldif",
        "slapcat -f /root/schema_convert.conf -F /root/kldif -n0 -s 'cn={0}kerberos,cn=schema,cn=config' > /root/kldif/cn=kerberos.ldif"
    )
    map(ssh_client.exec_shell_command, cmd_set)
    kerberos = os.path.join(TMP_DIR, "kerberos.ldif")
    dist_kerberos = "/root/kldif/cn=kerberos.ldif"
    with open(kerberos, "w") as f:
        f.write(KERBEROS)
    ssh_client.transport_file(kerberos, dist_kerberos)
    cmd_set = (
        "ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/cosine.ldif",
        "ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/misc.ldif",
        "ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/nis.ldif",
        "ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/inetorgperson.ldif",
        "ldapadd -Y EXTERNAL -H ldapi:/// -f /root/kldif/cn=kerberos.ldif",
        "ldapsearch -H ldapi:// -LLL -Q -Y EXTERNAL -b 'cn=schema,cn=config' dn"
    )
    map(ssh_client.exec_shell_command, cmd_set)

    stdin, stdout, stderr = ssh_client.ssh_client.exec_command("slappasswd", get_pty=True)
    stdin.write("gavial\n")
    stdin.flush()
    stdin.write("gavial\n")
    stdin.flush()
    ssha_key2 = stdout.readlines()[-1]

    basedn = os.path.join(RESOURCES_DIR, "basedn.ldif")
    ssh_client.transport_file(basedn, "/root/basedn.ldif")
    kdc_conf = os.path.join(RESOURCES_DIR, "kdc.conf")
    ssh_client.transport_file(kdc_conf, "/root/kdc.conf")

    chdomain = os.path.join(TMP_DIR, "chdomain.ldif")
    with open(chdomain, "w") as f:
        f.write(CHDOMAIN.replace("SSHA_KEY", ssha_key2))
    ssh_client.transport_file(chdomain, "/root/chdomain.ldif")

    ssh_client.exec_shell_command("ldapadd -Y EXTERNAL -H ldapi:/// -f /root/chdomain.ldif")
    stdin, stdout, stderr = ssh_client.ssh_client.exec_command(
        "ldapadd -x -D 'cn=admin,dc=mlogcn,dc=inn' -W -f /root/basedn.ldif",
        get_pty=True)
    stdin.write("gavial\n")
    stdin.flush()
    stdout.readlines()
    cmd_set = (
        "firewall-cmd --add-service=ldap --permanent",
        "firewall-cmd --reload",
        "ldapsearch -H ldapi:/// -LLL -Q -Y EXTERNAL -b 'dc=mlogcn,dc=inn' dn"
    )
    map(ssh_client.exec_shell_command, cmd_set)

    ssh_client.transport_file(os.path.join(TMP_DIR, "krb5.conf"), "/etc/krb5.conf")
    cmd_set = (
        "mkdir /etc/krb5kdc",
        "mv /root/kdc.conf /var/kerberos/krb5kdc/kdc.conf",
        "echo '*/admin@MLOGCN.INN *' > /var/kerberos/krb5kdc/kadm5.acl"
    )
    map(ssh_client.exec_shell_command, cmd_set)

    stdin, stdout, stderr = ssh_client.ssh_client.exec_command(
        "kdb5_ldap_util -D cn=admin,dc=mlogcn,dc=inn create -subtrees cn=container,dc=mlogcn,dc=inn -r MLOGCN.INN -s -H ldap://{0}".format(
            ip), get_pty=True)
    stdin.write("gavial\n")
    stdin.flush()
    stdin.write("gavial\n")
    stdin.flush()
    stdin.write("gavial\n")
    stdin.flush()
    print(stdout.readlines())
    stdin, stdout, stderr = ssh_client.ssh_client.exec_command(
        "kdb5_ldap_util -D cn=admin,dc=mlogcn,dc=inn stashsrvpw -f /etc/krb5kdc/service.keyfile cn=admin,dc=mlogcn,dc=inn",
        get_pty=True)
    stdin.write("gavial\n")
    stdin.flush()
    stdin.write("gavial\n")
    stdin.flush()
    stdin.write("gavial\n")
    stdin.flush()
    print(stdout.readlines())
    ssh_client.exec_shell_command("systemctl start krb5kdc & systemctl enable krb5kdc")
    ssh_client.exec_shell_command("systemctl start kadmin & systemctl enable kadmin")


def pythonldap(ssh_client):
    local_dir = os.path.join(RESOURCES_DIR, 'python-ldap')
    remote_dir = "/root/python-ldap".format(USER)
    ssh_client.transport_dir(local_dir, remote_dir)

    cmd_set = (
        RPM_IVH.format(os.path.join(remote_dir, "python-devel-2.7.5-34.el7.x86_64.rpm")),
        RPM_UVH.format(os.path.join(remote_dir, "cyrus-sasl-lib-2.1.26-20.el7_2.x86_64.rpm")),
        RPM_IVH.format(os.path.join(remote_dir, "cyrus-sasl-2.1.26-20.el7_2.x86_64.rpm")),
        RPM_IVH.format(os.path.join(remote_dir, "cyrus-sasl-devel-2.1.26-20.el7_2.x86_64.rpm")),
        RPM_IVH.format(os.path.join(remote_dir, "openldap-devel-2.4.40-13.el7.x86_64.rpm")),
        "tar zxf {0}".format(os.path.join(remote_dir, "python-ldap-2.4.32.tar.gz")),
        "cd {0};python setup.py install".format(os.path.join("/root", "python-ldap-2.4.32")),
        RPM_IVH.format(os.path.join(remote_dir, "krb5-workstation-1.14.1-27.el7_3.x86_64.rpm")),
        "tar zxf {0}".format(os.path.join(remote_dir, "Babel-2.4.0.tar.gz")),
        "cd {0};python setup.py install".format(os.path.join("/root", "Babel-2.4.0")),
        "tar zxf {0}".format(os.path.join(remote_dir, "click-6.6.tar.gz")),
        "cd {0};python setup.py install".format(os.path.join("/root", "click-6.6")),
        "tar zxf {0}".format(os.path.join(remote_dir, "itsdangerous-0.24.tar.gz")),
        "cd {0};python setup.py install".format(os.path.join("/root", "itsdangerous-0.24")),
        "tar zxf {0}".format(os.path.join(remote_dir, "MarkupSafe-1.0.tar.gz")),
        "cd {0};python setup.py install".format(os.path.join("/root", "MarkupSafe-1.0")),
        "tar zxf {0}".format(os.path.join(remote_dir, "Werkzeug-0.12.2.tar.gz")),
        "cd {0};python setup.py install".format(os.path.join("/root", "Werkzeug-0.12.2")),
        "tar zxf {0}".format(os.path.join(remote_dir, "Jinja2-2.9.6.tar.gz")),
        "cd {0};python setup.py install".format(os.path.join("/root", "Jinja2-2.9.6")),
        "tar zxf {0}".format(os.path.join(remote_dir, "Flask-0.12.tar.gz")),
        "cd {0};python setup.py install".format(os.path.join("/root", "Flask-0.12")),
    )
    map(ssh_client.exec_shell_command, cmd_set)


def kadmin_ldap_server(ssh_client, ldap_server):
    with open(os.path.join(RESOURCES_DIR, "kadmin_ldap_server/config.py"), "r") as f:
        ldap_config = f.read()
    with open(os.path.join(RESOURCES_DIR, "kadmin_ldap_server/config.py"), "w") as f:
        f.write(ldap_config.replace("LDAP_URI", ldap_server))

    local_dir = os.path.join(RESOURCES_DIR, 'kadmin_ldap_server')
    remote_dir = "/home/{0}/kadmin_ldap_server".format(USER)
    ssh_client.transport_dir(local_dir, remote_dir)


def mysql(ssh_client):
    mysql_path = os.path.join(RESOURCES_DIR, 'mysql.tar.gz')
    remote_path = "/root/mysql.tar.gz"
    ssh_client.transport_file(mysql_path, remote_path)
    ssh_client.exec_shell_command("tar zxf {0}".format(remote_path))

    stdin, stdout, stderr = ssh_client.ssh_client.exec_command(
        "yum remove mysql mysql-server mysql-libs", get_pty=True)
    stdin.write('y\n')
    stdin.flush()
    print(stdout.readlines())
    cmd_set = (
        RPM_IVH.format("/root/mysql/mysql-community-common-5.7.18-1.el7.x86_64.rpm"),
        RPM_IVH.format("/root/mysql/mysql-community-libs-5.7.18-1.el7.x86_64.rpm"),
        RPM_IVH.format("/root/mysql/mysql-community-client-5.7.18-1.el7.x86_64.rpm"),
        RPM_IVH.format("/root/mysql/mysql-community-server-5.7.18-1.el7.x86_64.rpm"),
        "mysqld --initialize --user=mysql",
    )
    map(ssh_client.exec_shell_command, cmd_set)

    print("install mysql seccuss")


def create_database(ssh_client):
    mysqld_log = "/var/log/mysqld.log"
    stdin, stdout, stderr = ssh_client.ssh_client.exec_command("cat {0}".format(mysqld_log))
    secret = ""
    for item in stdout.readlines():
        m = re.search("A temporary password is generated for root@localhost: (?P<secret>.+)", item)
        if m:
            secret = m.group("secret")
            break
    if secret == "":
        return
    ssh_client.exec_shell_command(
        "mysql -uroot -p{0} --connect-expired-password -e \"ALTER USER 'root'@'localhost' IDENTIFIED BY '123456';\"".format(
            secret))
    secret = "123456"
    ssh_client.exec_shell_command(
        "mysql -uroot -p{0} --connect-expired-password -e \"CREATE USER 'root'@'%' IDENTIFIED BY '123456';\"".format(
            secret))
    ssh_client.exec_shell_command(
        "mysql -uroot -p{0} --connect-expired-password -e \"CREATE USER 'hadoop'@'%' IDENTIFIED BY 'hadoop';\"".format(
            secret))
    ssh_client.exec_shell_command(
        "mysql -uroot -p{0} --connect-expired-password -e \"grant all on *.* to 'root'@'%';\"".format(secret))
    ssh_client.exec_shell_command(
        "mysql -uroot -p{0} --connect-expired-password -e \"grant all on *.* to 'hadoop'@'%';\"".format(secret))
    ssh_client.exec_shell_command(
        "mysql -uroot -p{0} --connect-expired-password -e \"flush privileges;\"".format(secret))
    ssh_client.exec_shell_command(
        "mysql -uroot -p{0} --connect-expired-password -e \"CREATE DATABASE gavial DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;\"".format(
            secret))
    ssh_client.exec_shell_command(
        "mysql -uroot -p{0} --connect-expired-password -e \"CREATE DATABASE azkaban DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;\"".format(
            secret))
    ssh_client.transport_file(os.path.join(RESOURCES_DIR, "create-all-sql-3.15.0.sql"),
                              "/root/create-all-sql-3.15.0.sql")
    ssh_client.exec_shell_command(
        "mysql -uroot -p{0} --connect-expired-password -e \"use azkaban;source /root/create-all-sql-3.15.0.sql;\"".format(
            secret))


def redis(ssh_client):
    redis_path = os.path.join(RESOURCES_DIR, 'redis-3.2.9.tar.gz')
    remote_path = "/home/{0}/{1}".format(USER, 'redis-3.2.9.tar.gz')
    ssh_client.transport_file(redis_path, remote_path)

    ssh_client.exec_shell_command("tar zxf {0}".format(remote_path))

    ssh_client.exec_shell_command("cd {0};make MALLOC=libc".format(REDIS_DEFAULT_PATH))

    stdin, stdout, stderr = ssh_client.ssh_client.exec_command("cd {0};sudo make install".format(REDIS_DEFAULT_PATH),
                                                               get_pty=True)
    stdin.write('{0}\n'.format(PASSWORD))
    stdin.flush()
    print(stdout.readlines())
    print("install redis seccuss")


def zookeeper(ssh_client, id):
    zk_path = os.path.join(RESOURCES_DIR, 'zookeeper-3.4.9.tar.gz')
    remote_path = "/home/{0}/{1}".format(USER, 'zookeeper-3.4.9.tar.gz')
    ssh_client.transport_file(zk_path, remote_path)
    ssh_client.exec_shell_command("tar zxf {0}".format(remote_path))

    ssh_client.transport_file(os.path.join(TMP_DIR, "zoo.cfg"), ZK_DEFAULT_CONF_PATH)
    ssh_client.exec_shell_command("mkdir {0}".format(ZOOKEEPER_TMP_DIR))
    ssh_client.exec_shell_command("echo {0} > {1}".format(id, os.path.join(ZOOKEEPER_TMP_DIR, "myid")))
    print("install zookeeper seccuss")


def hadoop(ssh_client):
    hadoop_path = os.path.join(RESOURCES_DIR, 'hadoop-2.7.3.tar.gz')
    remote_path = "/home/{0}/{1}".format(USER, 'hadoop-2.7.3.tar.gz')
    ssh_client.transport_file(hadoop_path, remote_path)

    ssh_client.exec_shell_command("tar zxf {0}".format(remote_path))

    ssh_client.exec_shell_command("mkdir {0}".format(HADOOP_TMP_DIR))
    ssh_client.exec_shell_command("mkdir /data1", use_root=True)
    ssh_client.exec_shell_command("mkdir /name1", use_root=True)
    src_path = (
        os.path.join(TMP_DIR, "hdfs-site.xml"),
        os.path.join(TMP_DIR, "core-site.xml"),
        os.path.join(TMP_DIR, "mapred-site.xml"),
        os.path.join(TMP_DIR, "yarn-site.xml"),
        os.path.join(TMP_DIR, "hadoop-slaves")
    )
    dist_path = (
        os.path.join(HADOOP_DEFAULT_CONF_PATH, "hdfs-site.xml"),
        os.path.join(HADOOP_DEFAULT_CONF_PATH, "core-site.xml"),
        os.path.join(HADOOP_DEFAULT_CONF_PATH, "mapred-site.xml"),
        os.path.join(HADOOP_DEFAULT_CONF_PATH, "yarn-site.xml"),
        os.path.join(HADOOP_DEFAULT_CONF_PATH, "slaves")
    )
    map(ssh_client.transport_file, src_path, dist_path)
    print("install hadoop seccuss")


def hive(ssh_client):
    hive_path = os.path.join(RESOURCES_DIR, 'hive-1.2.1.tar.gz')
    remote_path = "/home/{0}/{1}".format(USER, 'hive-1.2.1.tar.gz')
    ssh_client.transport_file(hive_path, remote_path)
    ssh_client.exec_shell_command("tar zxf {0}".format(remote_path))

    ssh_client.transport_file(os.path.join(TMP_DIR, "hive-site.xml"),
                              os.path.join(HIVE_DEFAULT_PATH, "conf/hive-site.xml"))
    ssh_client.transport_file(os.path.join(RESOURCES_DIR, "hive_aux.jar"),
                              os.path.join(HIVE_DEFAULT_PATH, "hive_aux.jar"))
    print("install hive seccuss")


def hbase(ssh_client):
    hbase_path = os.path.join(RESOURCES_DIR, 'hbase-1.2.4.tar.gz')
    remote_path = "/home/{0}/{1}".format(USER, 'hbase-1.2.4.tar.gz')
    ssh_client.transport_file(hbase_path, remote_path)
    ssh_client.exec_shell_command("tar zxf {0}".format(remote_path))

    src_path = (
        os.path.join(TMP_DIR, "hbase-site.xml"),
        os.path.join(TMP_DIR, "hbase-env.sh"),
        os.path.join(TMP_DIR, "hdfs-site.xml"),
        os.path.join(TMP_DIR, "core-site.xml"),
        os.path.join(TMP_DIR, "regionservers")
    )
    dist_path = (
        os.path.join(HBASE_DEFAULT_CONF_PATH, "hbase-site.xml"),
        os.path.join(HBASE_DEFAULT_CONF_PATH, "hbase-env.sh"),
        os.path.join(HBASE_DEFAULT_CONF_PATH, "hdfs-site.xml"),
        os.path.join(HBASE_DEFAULT_CONF_PATH, "core-site.xml"),
        os.path.join(HBASE_DEFAULT_CONF_PATH, "regionservers")
    )
    map(ssh_client.transport_file, src_path, dist_path)
    print("install hbase seccuss")


def presto(ssh_client):
    presto_path = os.path.join(RESOURCES_DIR, 'presto.tar.gz')
    remote_path = "/home/{0}/{1}".format(USER, 'presto.tar.gz')
    ssh_client.transport_file(presto_path, remote_path)
    ssh_client.exec_shell_command("tar zxf {0}".format(remote_path))
    src_path = (
        os.path.join(TMP_DIR, "config.properties"),
        os.path.join(TMP_DIR, "node.properties")
    )
    dist_path = (
        os.path.join(PRESTO_DEFAULT_CONF_PATH, "config.properties"),
        os.path.join(PRESTO_DEFAULT_CONF_PATH, "node.properties")
    )
    map(ssh_client.transport_file, src_path, dist_path)
    print("install presto seccuss")


def spark(ssh_client):
    spark_path = os.path.join(RESOURCES_DIR, 'spark-2.1.0.tar.gz')
    remote_path = "/home/{0}/{1}".format(USER, 'spark-2.1.0.tar.gz')
    ssh_client.transport_file(spark_path, remote_path)
    ssh_client.exec_shell_command("tar zxf {0}".format(remote_path))
    src_path = (
        os.path.join(TMP_DIR, "spark-env.sh"),
        os.path.join(TMP_DIR, "spark-defaults.conf"),
        os.path.join(TMP_DIR, "hive-site.xml"),
        os.path.join(TMP_DIR, "spark-slaves"),
    )
    dist_path = (
        os.path.join(SPARK_DEFAULT_CONF_PATH, "spark-env.sh"),
        os.path.join(SPARK_DEFAULT_CONF_PATH, "spark-defaults.conf"),
        os.path.join(SPARK_DEFAULT_CONF_PATH, "hive-site.xml"),
        os.path.join(SPARK_DEFAULT_CONF_PATH, "slaves")
    )
    map(ssh_client.transport_file, src_path, dist_path)
    print("install spark seccuss")


def azkaban(ssh_client):
    local_dir = os.path.join(RESOURCES_DIR, 'azkaban')
    remote_dir = "/home/{0}/azkaban".format(USER)
    ssh_client.transport_dir(local_dir, remote_dir)
    cmd_set = (
        "cd {0};tar zxf azkaban-exec-server-3.15.0-mlog.tar.gz".format(remote_dir),
        "cd {0};tar zxf azkaban-sql-3.15.0.tar.gz".format(remote_dir),
        "cd {0};tar zxf azkaban-web-server-3.15.0-mlog.tar.gz".format(remote_dir)
    )
    map(ssh_client.exec_shell_command, cmd_set)
    src_set = (
        os.path.join(TMP_DIR, "azkaban-web.properties"),
        os.path.join(TMP_DIR, "azkaban-exec.properties"),
        os.path.join(TMP_DIR, "commonprivate.properties")
    )
    dist_set = (
        os.path.join(AZKABAN_WEB_DEFAULT_PATH, "conf/azkaban.properties"),
        os.path.join(AZKABAN_EXEC_DEFAULT_PATH, "conf/azkaban.properties"),
        os.path.join(AZKABAN_EXEC_DEFAULT_PATH, "plugins/jobtypes/commonprivate.properties")
    )
    map(ssh_client.transport_file, src_set, dist_set)
    execute_exe = os.path.join(AZKABAN_EXEC_DEFAULT_PATH, "nativelib/execute-as-user")
    ssh_client.exec_shell_command("chown root {0}".format(execute_exe), use_root=True)
    ssh_client.exec_shell_command("chmod 6050 {0}".format(execute_exe), use_root=True)
