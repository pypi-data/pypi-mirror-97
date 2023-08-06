from src import config, upload, common
import requests, os, json


def view():
    project_list = common.get(common.get_cloud_base_url() + '/project/list?projectName=')

    for index, project in enumerate(project_list):
        print('Project id：' + str(index), '    Project name：' + project['name'])

    print('-----------Please select project id--------------')

    project_id = input()
    project = project_list[int(project_id)]

    cli_path = config.USER_BASE_PATH + '/' + config.cli_dir
    config_path = cli_path + '/' + config.cli_json
    config_json = {}
    with open(config_path, 'r', encoding='utf-8') as f:
        config_json = json.load(f)
    config_json['project_id'] = project['id']

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config_json, f, indent=2, sort_keys=True, ensure_ascii=False)

def getProjectId():
    cli_path = config.USER_BASE_PATH + '/' + config.cli_dir
    config_path = cli_path + '/' + config.cli_json
    config_json = {}
    with open(config_path, 'r', encoding='utf-8') as f:
        config_json = json.load(f)
    return config_json['project_id']

def checkProject():
    cli_path = config.USER_BASE_PATH + '/' + config.cli_dir
    config_path = cli_path + '/' + config.cli_json
    with open(config_path, 'r', encoding='utf-8') as f:
        config_json = json.load(f)

    if ('project_id' in config_json.keys()) is False:
        view()

    if ('project_id' in config_json.keys()) is True:
        cli_path = config.USER_BASE_PATH + '/' + config.cli_dir
        config_path = cli_path + '/' + config.cli_json
        config_json = {}
        with open(config_path, 'r', encoding='utf-8') as f:
            config_json = json.load(f)

        try:
            response = common.get(common.get_cloud_base_url() + '/project/info',
                                params={'projectId': config_json['project_id']})
            print('Current project:' + response['name'])
        except Exception as e:
            view()

