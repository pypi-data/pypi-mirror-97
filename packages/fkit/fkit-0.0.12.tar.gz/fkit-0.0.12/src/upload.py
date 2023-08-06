import json
import os

import oss2
import requests
from oss2 import SizedFileAdapter, determine_part_size
from oss2.models import PartInfo
import hashlib
import base64
import zlib

from src import config, project, common, log
myLogger = log.Logger()

def get_file_md5(file_name):
    """
    计算文件的md5
    :param file_name:
    :return:
    """
    m = hashlib.md5()   #创建md5对象
    with open(file_name,'rb') as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            m.update(data)  #更新md5对象

    return m.hexdigest()    #返回md5对象

def get_file_sha1(fineName):
    with open(fineName, 'rb') as f:
        sha1 = hashlib.sha1()
        while True:
            data = f.read(4096)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()


def get_file_crc32(file_path):
    prev = 0
    for eachLine in open(file_path, "rb"):
        prev = zlib.crc32(eachLine, prev)
    return str("%X" % (prev & 0xFFFFFFFF))

def upload(s=None, t=None):

    checkToken()
    if s is None:
        myLogger.error_logger('Please enter the correct file or directory')

    if t is None:
        myLogger.error_logger('Please enter the correct target upload directory')

    if not t.endswith('/'):
        myLogger.error_logger('Please enter the correct target upload directory')

    is_upload_dir = False
    is_upload_dir_file = False
    is_upload_file = False
    if s.endswith('/*') :
        t_s = s[:-1]
        is_dir = os.path.isdir(t_s)
        if is_dir:
            is_upload_dir_file = True
            # 检测目录或文件是否重复
            dir_files = os.listdir(t_s)  # 得到该文件夹下所有的文件
            for file in dir_files:
                file_path = os.path.join(t_s, file)  # 路径拼接成绝对路径
                if os.path.isfile(file_path):  # 如果是文件，就打印这个文件路径
                    temp_file_path = t + file_path.replace(t_s, "")

                    check_dir_or_file_exist(temp_file_path)
                if os.path.isdir(file_path):  # 如果目录，就递归子目录
                    temp_dir_path = t + file_path.replace(t_s, "") + '/'

                    check_dir_or_file_exist(temp_dir_path)
            uploadDir(t_s, t)
    elif s.endswith('/') :
        is_dir2 = os.path.isdir(s)
        if is_dir2 :
            is_upload_dir = True
            abs_path = os.path.abspath(s)
            print(os.path.split(abs_path))
            split_list = os.path.split(abs_path)
            last_dir_name = split_list[len(split_list) - 1]

            file_dir = t + last_dir_name+'/'
            check_dir_or_file_exist(file_dir)
            create_dir(last_dir_name, t)
            uploadDir(s, file_dir)
    else:
        is_file = os.path.isfile(s)
        if is_file:
            is_upload_file = True
            p, f = os.path.split(s)
            temp_path = t + f
            print("Check for duplicate files:" + temp_path)

            check_dir_or_file_exist(temp_path)
            uploadFile(s, t)

    if not is_upload_file and not is_upload_dir and not is_upload_dir_file:
        myLogger.error_logger('Please enter the correct file or directory')


def getToken():
    cli_path = config.USER_BASE_PATH + '/' + config.cli_dir
    config_path = cli_path + '/' + config.cli_json
    is_exist = os.path.exists(config_path)
    if not is_exist:
        myLogger.error_logger('Please login again')

    file = open(config_path, 'r')
    js = file.read()
    dic = json.loads(js)
    token = dic['access_token']
    file.close()

    return token

def uploadDir(dir, target_path):
    print("Upload folder:"+dir+",   Target path:"+target_path)

    for root, dirs, files in os.walk(dir):
        relative_path = root.replace(dir, "")
        path = target_path[:-1] + relative_path+'/'

        if not root.endswith('/'):
            root = root + '/'

        for temp_dir in dirs:
            create_dir(temp_dir, path)

        for file in files:
            abs_path = root + file

            temp_path = target_path + os.path.join(root, "")[len(dir):]
            uploadFile(abs_path, temp_path)

def check_dir_or_file_exist(dir_path):

    data = {
        "dirPath": dir_path,
        "projectId": project.getProjectId()
    }

    r = common.post(url=common.get_cloud_base_url() + '/file/checkFileOrDirExist', data=data)

def create_dir(dir_name, dir_path):

    data = {
        "name": dir_name,
        "dirPath": dir_path,
        "projectId": project.getProjectId()
    }

    r = common.post(url=common.get_cloud_base_url() + '/file/createDir',  data=data)


upload_total_size = 0
upload_uploaded_size = 0
def percentage(consumed_bytes, total_bytes):
    """进度条回调函数，计算当前完成的百分比

    :param consumed_bytes: 已经上传/下载的数据量
    :param total_bytes: 总数据量
    """
    if total_bytes:
        rate = 0
        if upload_total_size > 0:
            consumed_bytes = upload_uploaded_size + consumed_bytes
            rate = int(100 * (float(consumed_bytes) / float(upload_total_size)))
        if upload_total_size == 0:
            rate = 100
        print('\r{0}% '.format(rate), end='')

def uploadFile(file, target_path):
    print("Upload file: " + file)
    global upload_total_size
    upload_total_size = 0
    global upload_uploaded_size
    upload_uploaded_size = 0
    file_name = os.path.basename(file)
    file_path = os.path.abspath(file)
    total_size = os.path.getsize(file_path)

    md5_value = get_file_md5(file_path)
    sha1_value = get_file_sha1(file_path)
    crc32_value = get_file_crc32(file_path)
    print(md5_value)
    print(sha1_value)
    print(crc32_value)
    body = {
        "name": file_name,
        "type": 1,
        "dirPath": target_path,
        "projectId": project.getProjectId(),
        "md5": md5_value,
        "sha1": sha1_value,
        "crc32": crc32_value
    }

    data = common.post(url=common.get_cloud_base_url() + '/file/uploadFile', data=body)

    file_id = data['fileId']
    oss_path = data['ossPath']
    oss_endpoint = data['ossEndpoint']
    oss_bucket_name = data['ossBucketName']
    key = 'file/'+oss_path
    passUpload = data["passUpload"]

    if passUpload == 0:
        auth = oss2.StsAuth(data['accessKeyId'], data['accessKeySecret'], data['securityToken'])
        bucket = oss2.Bucket(auth, oss_endpoint, oss_bucket_name)

        # print("CPU的核数为：{}".format(cpu_count()))
        # determine_part_size方法用于确定分片大小。

        # 20M 一块
        if total_size < 1024:
            print("File size: "+str(int(total_size)) +"B")
        elif total_size <= 1024 * 1024:
            print("File size: "+str(int(total_size/1024)) +"KB")
        elif total_size <= 1024 * 1024 * 1024:
            print("File size: "+str(int(total_size/1024/1024)) +"MB")
        else:
            print("File size: " + str(int(total_size / 1024 / 1024 / 1024)) + "GB")

        upload_total_size = total_size
        if(total_size > 1024*1024*20):
            part_size = determine_part_size(total_size, preferred_size=(1024*1024*20))

            # 初始化分片。
            # 如需在初始化分片时设置文件存储类型，请在init_multipart_upload中设置相关headers，参考如下。
            # headers = dict()
            # headers["x-oss-storage-class"] = "Standard"
            # upload_id = bucket.init_multipart_upload(key, headers=headers).upload_id
            upload_id = bucket.init_multipart_upload(key).upload_id
            parts = []

            with open(file_path, 'rb') as fileobj:

                # 逐个上传分片。
                part_number = 1
                offset = 0
                while offset < total_size:
                    num_to_upload = min(part_size, total_size - offset)
                    # 调用SizedFileAdapter(fileobj, size)方法会生成一个新的文件对象，重新计算起始追加位置。
                    result = bucket.upload_part(key, upload_id, part_number,
                                                SizedFileAdapter(fileobj, num_to_upload), progress_callback=percentage)
                    parts.append(PartInfo(part_number, result.etag))

                    offset += num_to_upload
                    upload_uploaded_size = offset
                    part_number += 1
            # 完成分片上传。
            # 如需在完成分片上传时设置文件访问权限ACL，请在complete_multipart_upload函数中设置相关headers，参考如下。
            # headers = dict()
            # headers["x-oss-object-acl"] = oss2.OBJECT_ACL_PRIVATE
            # bucket.complete_multipart_upload(key, upload_id, parts, headers=headers)

            bucket.complete_multipart_upload(key, upload_id, parts)

            # 验证分片上传。
            with open(file_path, 'rb') as fileobj:
                assert bucket.get_object(key).read() == fileobj.read()

        else:
            bucket.put_object_from_file(key, file_path, progress_callback=percentage)

    needInsertVerify = 1
    if(passUpload == 1) :
        needInsertVerify = 0
    # 上传完毕后更新文件状态
    params = {
        'fileId': file_id,
        'status': 1,
        'projectId': project.getProjectId(),
        'needInsertVerify': needInsertVerify,
        'md5': md5_value,
        'sha1': sha1_value,
        'crc32': crc32_value
    }

    data = common.post(url=common.get_cloud_base_url() + '/file/uploadFileFinish', data=params)
    print(data)
    if(data['status'] == 1):
        if passUpload == 1:
            print(file_path + "   Quick upload complete")
        else :
            print(file_path + "   Upload complete")
    elif data['status'] == 0:
        print(file_path+"   Upload failed. There is a file with the same name in the same directory")


def checkToken():
    params = {'token': getToken()}

    r = common.post(url=common.get_login_base_url() + '/user/check/token', data=params)
