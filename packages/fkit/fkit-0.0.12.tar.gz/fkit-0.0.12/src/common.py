import json
import os
import requests

from src import config, codeMsg

from src import log
myLogger = log.Logger()

def getCodeMsg(msgCode):
    return codeMsg.msg[msgCode]


def get_login_base_url(env=None):
    if env == None:
        env = getEnv()

    if env == 'develop':
        return config.login_base_url_develop
    elif env == 'stage':
        return config.login_base_url_stage
    elif env == 'master':
        return config.login_base_url_master


def get_cloud_base_url(env=None):
    if env == None:
        env = getEnv()
    if env == 'develop':
        return config.cloud_base_url_develop
    elif env == 'stage':
        return config.cloud_base_url_stage
    elif env == 'master':
        return config.cloud_base_url_master


def get_docker_registry(env=None):
    if env == None:
        env = getEnv()
    if env == 'develop':
        return config.docker_registry_develop
    elif env == 'stage':
        return config.docker_registry_stage
    elif env == 'master':
        return config.docker_registry_master



def getEnv():
    cli_path = config.USER_BASE_PATH + '/' + config.cli_dir
    config_path = cli_path + '/' + config.cli_json
    is_exist = os.path.exists(config_path)
    if not is_exist:
        myLogger.error_logger('Please login again')

    file = open(config_path, 'r')
    js = file.read()
    dic = json.loads(js)
    env = dic['env']
    if env == "":
        myLogger.error_logger("Please login again")
    file.close()

    return env

# -----------------授权相关 start-------------------------------------------------
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
    if token == "":
        myLogger.error_logger("Please login again")
    file.close()

    return token

def checkToken(token=None, env=None):
    if token is not None:
        params = {'token': token}
        post(url=get_login_base_url(env) + '/user/check/token', data=params, haveToken=False)
    else:
        params = {'token': getToken()}
        post(url=get_login_base_url(env) + '/user/check/token', data=params, haveToken=False)


# -----------------授权相关 end-------------------------------------------------

# ----------------数据请求相关 end-------------------------------------------------

def get(url, params=None, haveToken=True):
    if haveToken == True:
        token = getToken()
        response = requests.get(url=url, params=params, headers={
            'Content-Type': 'application/json',
            'ACCESS_TOKEN': token
        })
        return dealResponse(response=response)
    if haveToken == False:
        response = requests.get(url=url, params=params, headers={
            'Content-Type': 'application/json',
        })
        return dealResponse(response=response)


def post(url, data, haveToken=True):
    if haveToken == True:
        token = getToken()
        response = requests.post(url=url, data=json.dumps(data), headers={
            'Content-Type': 'application/json',
            'ACCESS_TOKEN': token
        })
        return dealResponse(response=response)

    if haveToken == False:
        response = requests.post(url=url, data=json.dumps(data), headers={
            'Content-Type': 'application/json'
        })
        return dealResponse(response=response)

def dealResponse(response):
    if response.status_code == 200:
        return response.json()['data']
    if response.status_code == 401:
        myLogger.error_logger("Authorization failed, please login again")
        
    if response.status_code >= 400 and response.status_code < 500:
        resJson = response.json()
        value = getCodeMsg(str(resJson['msgCode']))
        myLogger.error_logger(value)

    if response.status_code >= 500:
        resJson = response.json()
        value = getCodeMsg(str(resJson['msgCode']))
        myLogger.error_logger(value)