import os
from src import config


def logout():
    cli_path = config.USER_BASE_PATH + '/' + config.cli_dir + '/' + config.cli_json
    is_exist = os.path.exists(cli_path)
    if is_exist:
        os.remove(cli_path)
    print("Logout successfully")