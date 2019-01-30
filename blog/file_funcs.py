#!/usr/bin/env python
# _*_coding:utf-8_*_

"""
@Time :  2018/12/16 23:03
@Author:  zhao
@File: file_funcs.py
@Software: PyCharm
@Description: 
"""
import os
import paramiko
from django.core.files.storage import FileSystemStorage
import uuid

from djangoblog import settings


class ImageStorage(FileSystemStorage):
    from django.conf import settings

    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        # 初始化
        super(ImageStorage, self).__init__(location, base_url)

    # 重写 _save方法
    def _save(self, name, content):
        # name为上传文件名称
        import os
        # 文件扩展名
        ext = os.path.splitext(name)[1]
        file_name = os.path.basename(name)
        # 文件目录
        fn = get_uuid(file_name)
        # windows和linux下链接路径的符号不同所以
        # name = os.path.join('/sites/nogizaka46/images', fn + ext)
        name = settings.IMAGE_SAVING_PATH + fn + ext
        write_file(content,name,settings.UPLOAD_HOST,settings.HOST_USER,settings.HOST_PASSWORD,22)
        return 'blog/images/' + fn + ext


# 执行命令/删除
def exec_command(comm, hostname, username, password):
    ssh = paramiko.SSHClient()
    # 使用密钥登陆Linux
    ssh.load_system_host_keys()
    privatekey = os.path.expanduser(password)
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    key = paramiko.RSAKey.from_private_key_file(privatekey)

    ssh.connect(hostname=hostname, username=username, password=password)
    stdin, stdout, stderr = ssh.exec_command(comm)
    result = stdout.read() + stderr.read()
    # print(result.decode('utf-8'))
    ssh.close()
    return result


#写文件
def write_file(file, remote_path, hostname, username, password, port=22):
    ssh = paramiko.SSHClient()
    # 使用密钥登陆Linux
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, username=username, password=password, port=port)
    # 先创建
    comm = "touch " + remote_path
    print(comm)
    ssh.exec_command(comm)
    t = ssh.get_transport()
    sftp = paramiko.SFTPClient.from_transport(t)

    # file 是InMemoryUploadedFile
    source = file.open()
    try:
        all_text = source.read()
    finally:
        file.close()
    remote_file = sftp.open(remote_path, 'w+')
    try:
        remote_file.write(all_text)
    finally:
        remote_file.close()


def get_uuid(name):
    return str(uuid.uuid3(uuid.NAMESPACE_URL,name)).replace("-","")