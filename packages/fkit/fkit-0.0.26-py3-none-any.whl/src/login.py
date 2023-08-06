import json
from src import common, config, project, log
import getpass, os
myLogger = log.Logger()

def login(k, env):
    cli_path = config.USER_BASE_PATH + '/' + config.cli_dir
    config_path = cli_path + '/' + config.cli_json
    config_json = {}
    if env == None:
        env = 'master'
    else:
        if env != 'develop' and env != 'stage' and env != 'master':
            myLogger.error_logger("error env")

    if k is None:
        print("Please enter your email address")
        account = input()
        password = getpass.getpass("Please enter your password")

        data = {
            "email": account,
            "password": password
        }
        response = common.post(url=common.get_login_base_url(env) + '/user/login', haveToken=False, data=data)
        token = response['token']
        cli_path = config.USER_BASE_PATH + '/' + config.cli_dir

        print(cli_path)
        is_exist = os.path.exists(cli_path)
        if not is_exist:
            os.makedirs(cli_path)

        config_path = cli_path + '/' + config.cli_json
        json_exist = os.path.exists(config_path)
        if json_exist:
           os.remove(config_path)

        config_json['access_token'] = token
        config_json['env'] =env
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_json, f, indent=2, sort_keys=True, ensure_ascii=False)

        print("login successful")
        project.checkProject()

    if k is not None:
        common.checkToken(token=k, env=env)
        token = k
        cli_path = config.USER_BASE_PATH + '/' + config.cli_dir
        is_exist = os.path.exists(cli_path)
        if not is_exist:
            os.makedirs(cli_path)

        config_path = cli_path + '/' + config.cli_json
        json_exist = os.path.exists(config_path)
        if json_exist:
            os.remove(config_path)
        config_json['access_token'] = token
        config_json['env'] = env
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config_json, f, indent=2, sort_keys=True, ensure_ascii=False)

        print("login successful")
        project.checkProject()
