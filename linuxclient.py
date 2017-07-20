# encoding: utf-8
from __future__ import print_function
import paramiko
import os


class LinuxClient(object):
    def __init__(self, host, username='root', password=None, port=22, timeout=30, key_path=None):
        self.host = host
        self.password = password
        self.username = username
        self.port = port
        self.timeout = timeout
        self.retrys = 3
        self.key_path = key_path
        self.ssh_client = self.create_ssh_client()
        print("create ssh client over")

    def create_ssh_client(self):
        ssh_client = paramiko.SSHClient()
        ssh_client.load_system_host_keys()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        while True:
            try:
                if self.password is None and self.key_path is not None:
                    key = paramiko.RSAKey.from_private_key_file(self.key_path)
                    ssh_client.connect(hostname=self.host, port=self.port, username=self.username, pkey=key)
                else:
                    ssh_client.connect(hostname=self.host, port=self.port, username=self.username,
                                       password=self.password)
                return ssh_client
            except Exception as e:
                if self.retrys > 0:
                    self.retrys -= 1
                else:
                    return None
                print("connect {0} error, {1}".format(self.host, e))

    def release(self):
        if self.ssh_client is not None:
            self.ssh_client.close()
            self.ssh_client = None

    def exec_shell_command(self, command_str, use_root=False):
        if self.username != "root" and use_root:
            command_str = "sudo {0}".format(command_str)
            stdin, stdout, stderr = self.ssh_client.exec_command(command=command_str, get_pty=True)

            stdin.write('{0}\n'.format(self.password))
            stdin.flush()
        else:
            stdin, stdout, stderr = self.ssh_client.exec_command(command=command_str)
        print("--------------------------")
        print("cmd:" + command_str)
        print("error")
        print(stderr.readlines())
        print("out")
        print(stdout.readlines())

    def transport_file(self, local_path, remote_path):
        try:
            trans = paramiko.Transport((self.host, self.port))
            if self.password is None and self.key_path is not None:
                key = paramiko.RSAKey.from_private_key_file(self.key_path)
                trans.connect(username=self.username, pkey=key)
            else:
                trans.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(trans)
            sftp.put(local_path, remote_path)
            sftp.close()
            trans.close()
            print(local_path + "    to     " + remote_path)
        except Exception as e:
            print("transport file error, {0}".format(e))

    def transport_file2local(self, local_path, remote_path):
        try:
            trans = paramiko.Transport((self.host, self.port))
            if self.password is None and self.key_path is not None:
                key = paramiko.RSAKey.from_private_key_file(self.key_path)
                trans.connect(username=self.username, pkey=key)
            else:
                trans.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(trans)
            sftp.get(remote_path, local_path)
            sftp.close()
            trans.close()
            print(remote_path + "    to     " + local_path)
        except Exception as e:
            print("transport file error, {0}".format(e))

    def transport_dir(self, local_dir, remote_dir):
        try:
            trans = paramiko.Transport((self.host, self.port))
            if self.password is None and self.key_path is not None:
                key = paramiko.RSAKey.from_private_key_file(self.key_path)
                trans.connect(username=self.username, pkey=key)
            else:
                trans.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(trans)
            self.recursive_dir(local_dir, remote_dir, sftp)
            sftp.close()
            trans.close()
        except Exception as e:
            print("transport dir error, {0}".format(e))

    def recursive_dir(self, local_dir, remote_dir, sftp):
        sftp.mkdir(remote_dir)
        for root, dirs, files in os.walk(local_dir):
            for file_name in files:
                local_file = os.path.join(root, file_name)
                remote_file = os.path.join(remote_dir, file_name)
                try:
                    sftp.put(local_file, remote_file)
                except Exception as e:
                    sftp.mkdir(os.path.split(remote_file)[0])
                    sftp.put(local_file, remote_file)
            for dir_name in dirs:
                local_path = os.path.join(root, dir_name)
                remote_path = os.path.join(remote_dir, dir_name)
                self.recursive_dir(local_path, remote_path, sftp)
