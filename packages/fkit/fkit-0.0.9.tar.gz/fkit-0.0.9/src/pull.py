from src import common, config, project, log
import os, json, docker
myLogger = log.Logger()

template = {
    "id": "",
    "name": "",
    "desc": "",
    "cmd": '''''',
    "imageName": "",
    "inputs": [
        {
            "label": "",
            "key": "",
            "name": ""
        }
    ],
    "outputs": [
        {
            "label": "",
            "key": "",
            "name": ""
        }
    ]
}

def pull(toolVersionId):

    pullToolEntity = common.get(url=common.get_cloud_base_url() + '/tool/toolversion/id', params={'id': toolVersionId, 'projectId': project.getProjectId()})
    if pullToolEntity is None:
        myLogger.error_logger('The tool version id error')
    toolEntity = common.get(url=common.get_cloud_base_url() + '/tool/tool/id', params={'id': pullToolEntity['id'], 'projectId': project.getProjectId()})
    print(toolEntity)
    if toolEntity is None:
        myLogger.error_logger("Tool does not exist")

    print(toolEntity['name'])
    template['name'] = toolEntity['name']
    template['desc'] = pullToolEntity['desc']
    template['id'] = toolEntity['id']
    auth = common.get(url=common.get_cloud_base_url() + '/tool/pass')
    client = docker.from_env()
    client.images.pull(repository=common.get_docker_registry() + '/' + pullToolEntity['path'],
                       tag="latest",
                       auth_config={'username': auth['account'], 'password': auth['password']})
    image = client.images.get(common.get_docker_registry() + '/' + pullToolEntity['path'] + ':latest')
    image.tag(repository=toolEntity['id'], tag=str(pullToolEntity['version']))
    client.images.remove(common.get_docker_registry() + '/' + pullToolEntity['path'] + ':latest')
    template['imageName'] = toolEntity['id'] + ':' + str(pullToolEntity['version'])
    template['inputs'] = pullToolEntity['inputs']
    template['outputs'] = pullToolEntity['outputs']
    template['version'] = pullToolEntity['version']

    tempStr = json.dumps(template, indent=4, ensure_ascii=False)
    tempStr = tempStr.replace("\"cmd\": \"\"", "\"cmd\": '''" + pullToolEntity['cmd'] + "'''")
    with open(os.getcwd() + '/tool.py', 'w', encoding='utf-8') as f:
        f.write(tempStr)
    os.mkdir(os.getcwd() + '/input')
    os.mkdir(os.getcwd() + '/output')