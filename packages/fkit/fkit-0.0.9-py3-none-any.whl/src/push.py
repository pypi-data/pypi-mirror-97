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
            myLogger.error_logger('Please enter the correct tool.json')
        with open(file, 'r', encoding='utf-8') as f:
            str = f.read()
            config_json = ast.literal_eval(str)
            checkToolConfig(config_json)
        pushImage(config_json)

def pushImage(config_json):
    if config_json['id'] == '':
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

    print("===========================toolVersionCmdParamList===========================")
    print(toolVersionCmdParamList)
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

    outLabelSet = set()
    outFileKeyList = set()
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
            if '*' in outFile['name']:
                myLogger.error_logger('Output command line arguments are not available *')
            outFileKeyList.add(outFile['key'])
            outFileKeyLength = outFileKeyLength + 1

    if inFileKeyLength != len(inFileKeyList):
        myLogger.error_logger("The input file key cannot be repeated")
    if outFileKeyLength != len(outFileKeyList):
        myLogger.error_logger("The output file key cannot be repeated")

    toolVersionParamsInFileKeySet = set()
    for toolVersionCmdParam in toolVersionCmdParamList:
        if toolVersionCmdParam['type'] == 2:
            toolVersionParamsInFileKeySet.add(toolVersionCmdParam['paramKey'])

    toolVersionParamsOutFileKeySet = set()
    for toolVersionCmdParam in toolVersionCmdParamList:
        if toolVersionCmdParam['type'] == 3:
            toolVersionParamsOutFileKeySet.add(toolVersionCmdParam['paramKey'])

    isInFileEqual = inFileKeyList.difference(toolVersionParamsInFileKeySet)
    if len(isInFileEqual) != 0:
        myLogger.error_logger('Input key and cmd key do not match')

    isOutFileEqual = outFileKeyList.difference(toolVersionParamsOutFileKeySet)
    if len(isOutFileEqual) != 0:
        myLogger.error_logger('Output key and cmd key do not match')

def analysis(cmd):
    response = common.get(url=common.get_cloud_base_url() + '/tool/analysis/cmd', params={"cmd": cmd})
    return response

