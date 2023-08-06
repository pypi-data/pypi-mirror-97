import os

version = '0.0.8'

# 开发
login_base_url_develop = 'http://develop.tentech.com.cn:8080'
cloud_base_url_develop = 'http://develop.tentech.com.cn:8081'
docker_registry_develop = 'develop.tentech.com.cn:5000'

# 测试
login_base_url_stage = 'http://stage.tentech.com.cn:8080'
cloud_base_url_stage = 'http://stage.tentech.com.cn:8081'
docker_registry_stage = 'stage.tentech.com.cn:5000'

# 生产
login_base_url_master = 'http://www.flowhub.com.cn:8080'
cloud_base_url_master = 'http://www.flowhub.com.cn:8081'
docker_registry_master = 'tool.flowhub.com.cn:5000'

cli_dir = '.cli'
USER_BASE_PATH = os.path.expanduser('~')
cli_json = '.cli.json'

oss_file_path = 'file/'
