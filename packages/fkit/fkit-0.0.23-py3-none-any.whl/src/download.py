import os

import oss2
import requests
from src import common, config, project, log
myLogger = log.Logger()


def download(s=None, t=None):
    common.checkToken()

    if s is None:
        myLogger.error_logger('Please enter the correct file or directory')

    if t is None:
        myLogger.error_logger('Please enter the correct directory')

    if not t.endswith("/"):
        myLogger.error_logger('Please enter the correct directory')

    if s.endswith("/"):
        downloadDir(s, t)
    else:
        downloadFile(s, t)

def downloadDir(s=None, t=None):
    print("Directory download: "+s)
    data = {
        "dirPath": s,
        "projectId": project.getProjectId()
    }

    data = common.get(url=common.get_cloud_base_url() + '/file/getFilesByDirPath',params=data)

    for index in range(len(data)):
        if(data[index]['type'] == 0):
            temp_relative_path = t +data[index]['relativePath']

            abs_path = os.path.abspath(temp_relative_path)

            if(not os.path.isdir(abs_path)):
                print("Directory does not exist, create directory, path:"+abs_path)
                os.makedirs(abs_path)

        elif(data[index]['type'] == 1):
            temp_path = data[index]['path']
            temp_name = data[index]['name']

            t_path = t+data[index]['relativePath']

            t_path = t_path[0: len(t_path) - len(temp_name)]
            abs_path = os.path.abspath(t_path)
            downloadFile(temp_path, abs_path)

def downloadFile(s=None, t=None):
    print('Download file: '+s)
    data = {
        "filePath": s,
        "projectId": project.getProjectId()
    }


    data = common.get(url=common.get_cloud_base_url() + '/file/downloadFile', params=data)

    oss_path = data['ossPath']
    file_name = data['name']
    oss_endpoint = data['ossEndpoint']
    oss_bucket_name = data['ossBucketName']
    download_file_path = t+'/'+file_name
    if os.path.isfile(download_file_path):
        print("There is already a file with the same name locally, skip downloading the file")
    else:
        def percentage(consumed_bytes, total_bytes):
            if total_bytes:
                rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
                print('\rDownload progress {0}% '.format(rate), end='')

        auth = oss2.StsAuth(data['accessKeyId'], data['accessKeySecret'], data['securityToken'])
        bucket = oss2.Bucket(auth, oss_endpoint, oss_bucket_name)

        # 判断文件是否存在,存在跳过，提示用户

        bucket.get_object_to_file(config.oss_file_path + oss_path, download_file_path, progress_callback=percentage);
