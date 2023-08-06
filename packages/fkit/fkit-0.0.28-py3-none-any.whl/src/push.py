import json
import os
import re
import uuid
import docker
import ast

from src import common, config, project, log
myLogger = log.Logger()

def push(file):

    if file is None:
        is_exist = os.path.exists(os.getcwd() + '/tool.py')
        if is_exist == False:
            myLogger.error_logger('Please initialize the tool')
        with open(os.getcwd() + '/tool.py', 'r', encoding='utf-8') as f:
            str = f.read()
            config_json = ast.literal_eval(str)
            checkToolConfig(config_json)

        pushImage(config_json)

    if file is not None:
        file = file.strip()
        is_exist = os.path.exists(file)
        if is_exist == False:
            myLogger.error_logger('Please enter the correct tool.py')
        with open(file, 'r', encoding='utf-8') as f:
            str = f.read()
            config_json = ast.literal_eval(str)
            checkToolConfig(config_json)
        pushImage(config_json)
    print("push successful")


def pushImage(config_json):
    if config_json['id'] == '':
        imageName = config_json['imageName']
        client = docker.from_env(timeout=100000000)
        image = client.images.get(imageName)
        path = str(uuid.uuid1()).replace("-", "")

        image.tag(common.get_docker_registry() + '/' + path, tag='latest')
        auth = common.get(url=common.get_cloud_base_url() + '/tool/pass')
        for line in client.images.push(common.get_docker_registry() + '/' + path, auth_config={'username': auth['account'], 'password': auth['password']}, stream=True, decode=True):
            print(line)
            if 'error' in line and line['error'] != '':
                print(line['error'])
                client.images.remove(common.get_docker_registry() + '/' + path + ':latest')
                myLogger.error_logger('Tool upload failed')
            if 'progressDetail' in line and (line['progressDetail'] != '' and line['progressDetail'] != {} and 'current' in line['progressDetail'] and 'total' in line['progressDetail']):
                current = line['progressDetail']['current']
                total = line['progressDetail']['total']
                if current > total:
                    current = total
                progress_num = (current / total)*100
                progress = round(progress_num, 2)
                print('uploading: '+str(progress)+"%")
        try:
            common.post(url=common.get_cloud_base_url() + '/tool/create', data={
                'name': config_json['name'],
                'desc': config_json['desc'],
                'cmd': config_json['cmd'],
                'inputs': config_json['inputs'],
                'outputs': config_json['outputs'],
                'path': path,
                'projectId': project.getProjectId()
            })
        except Exception as e:
            print(e)
        client.images.remove(common.get_docker_registry() + '/' + path + ':latest')
    if config_json['id'] != '':
        imageName = config_json['imageName']
        client = docker.from_env()
        image = client.images.get(imageName)
        path = str(uuid.uuid1()).replace("-", "")

        image.tag(common.get_docker_registry() + '/' + path, tag='latest')
        auth = common.get(url=common.get_cloud_base_url() + '/tool/pass')
        for line in client.images.push(common.get_docker_registry() + '/' + path, auth_config={'username': auth['account'], 'password': auth['password']}, stream=True, decode=True):
            if 'error' in line and line['error'] != '':
                print(line['error'])
                client.images.remove(common.get_docker_registry() + '/' + path + ':latest')
                myLogger.error_logger('Tool upload failed')
            print(line)
        try:
            common.post(url=common.get_cloud_base_url() + '/tool/create/version', data={
                'name': config_json['name'],
                'desc': config_json['desc'],
                'cmd': config_json['cmd'],
                'inputs': config_json['inputs'],
                'outputs': config_json['outputs'],
                'path': path,
                'id': config_json['id'],
                'projectId': project.getProjectId()
            })
        except Exception as e:
            print(e)
        client.images.remove(common.get_docker_registry() + '/' + path + ':latest')


def checkToolConfig(toolConfig):
    if toolConfig['imageName'] == '':
        myLogger.error_logger('Please enter the correct image name')
    if toolConfig['imageName'] != '':
        client = docker.from_env()
        images = client.images
        images.get(toolConfig['imageName'])
    if toolConfig['cmd'] == '':
        myLogger.error_logger("Command cannot be empty")
    if toolConfig['id'] == '':
        toolName = toolConfig['name']
        response = common.get(url=common.get_cloud_base_url() + '/tool/name', params={"name": toolName, "projectId": project.getProjectId()})
        if response is not None:
            myLogger.error_logger("Tool already exists, please do not submit again")
    toolVersionCmdParamList = []
    if toolConfig['cmd'] != '':
        toolVersionCmdParamList = analysis(cmd=toolConfig['cmd'])

    have_in_dir = False
    have_out_dir = False
    for cmdParam in toolVersionCmdParamList:
        if cmdParam['type'] == 4:
            have_in_dir = True
        if cmdParam['type'] == 5:
            have_out_dir = True

    toolInputFileList = toolConfig['inputs']

    inLabelSet = set()
    inFileKeyList = set()
    inFileKeyLength = 0
    for inputFile in toolInputFileList:
        if inputFile['label'] == '':
            myLogger.error_logger('Label cannot be blank')
        inLabelSet.add(inputFile['label'])
        if inputFile['key'] != '':
            inFileKeyList.add(inputFile['key'])
            inFileKeyLength = inFileKeyLength + 1
        else:
            if not have_in_dir:
                myLogger.error_logger('CMD does not match the parameter')

    outLabelSet = set()
    outFileKeyList = set()
    outDirFileSet = set()
    outFileKeyLength = 0
    toolOutputFileList = toolConfig['outputs']
    if len(toolOutputFileList) == 0:
        myLogger.error_logger('outputs cannot be empty')
    for outFile in toolOutputFileList:
        if outFile['name'] == '' or outFile['name'] is None:
            myLogger.error_logger('The output file name cannot be blank')

        if outFile['label'] == '':
            myLogger.error_logger('Label cannot be blank')

        outLabelSet.add(outFile['label'])
        if outFile['key'] != '':
            if '*' is outFile['name']:
                myLogger.error_logger('Output command line arguments are not available *')
            outFileKeyList.add(outFile['key'])
            outFileKeyLength = outFileKeyLength + 1
        else:
            if not have_out_dir:
                myLogger.error_logger('CMD does not match the parameter')

        if outFile['key'] == '' and '*' in outFile['name']:
            if outFile['name'].startswith('*.'):
                out_file_str_list = outFile['name'].split('.')
                if len(out_file_str_list) == 2:
                    myLogger.error_logger('OutName error')
                else:
                    if out_file_str_list[1] == '':
                        myLogger.error_logger('OutName error')
                    else:
                        if outFile['name'] in outDirFileSet:
                            myLogger.error_logger('Output file name repeat')
                        else:
                            outDirFileSet.add(outFile['name'])


    if inFileKeyLength != len(inFileKeyList):
        myLogger.error_logger("The input file key cannot be repeated")
    if outFileKeyLength != len(outFileKeyList):
        myLogger.error_logger("The output file key cannot be repeated")

    toolVersionParamsInFileKeySet = set()
    for toolVersionCmdParam in toolVersionCmdParamList:
        if toolVersionCmdParam['type'] == 2:
            toolVersionParamsInFileKeySet.add(toolVersionCmdParam['paramKey'])

    if len(toolVersionParamsInFileKeySet) == 0 and inFileKeyLength > 0:
        myLogger.error_logger('input error')


    toolVersionParamsOutFileKeySet = set()
    for toolVersionCmdParam in toolVersionCmdParamList:
        if toolVersionCmdParam['type'] == 3:
            toolVersionParamsOutFileKeySet.add(toolVersionCmdParam['paramKey'])

    if len(toolVersionParamsOutFileKeySet) == 0 and outFileKeyLength > 0:
        myLogger.error_logger('output error')

    isInFileEqual = inFileKeyList.difference(toolVersionParamsInFileKeySet)
    if len(isInFileEqual) != 0:
        myLogger.error_logger('Input key and cmd key do not match')

    isOutFileEqual = outFileKeyList.difference(toolVersionParamsOutFileKeySet)
    if len(isOutFileEqual) != 0:
        myLogger.error_logger('Output key and cmd key do not match')

def analysis(cmd):
    response = common.get(url=common.get_cloud_base_url() + '/tool/analysis/cmd', params={"cmd": cmd})
    return response

