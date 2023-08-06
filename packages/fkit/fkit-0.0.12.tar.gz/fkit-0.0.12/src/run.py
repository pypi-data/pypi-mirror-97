import docker, os, json, re
from src import push, log
myLogger = log.Logger()

def run():

    configJsonExist = os.path.exists(os.getcwd() + '/tool.json')
    if not configJsonExist:
        myLogger.error_logger("The tool.json file cannot be found, please make sure to execute the command in the correct path")

    inputExist = os.path.exists(os.getcwd() + '/input')
    outputExist = os.path.exists(os.getcwd() + '/output')
    if not inputExist:
        myLogger.error_logger("Missing input folder, please create \"input\" folder in execution path")
    if not outputExist:
        myLogger.error_logger("Missing output folder, please create \"output\" folder in execution path")
    with open(os.getcwd() + '/tool.json', 'r', encoding='utf-8') as f:
        config_json = json.load(f)
        push.checkToolConfig(config_json)
        cmdParams = push.analysis(config_json['cmd'])
        taskCmdParamEntityList = cmdParams

    taskCmd = config_json['cmd']
    inputs = []
    for input in config_json['inputs']:
        input['type'] = 0
        inputs.append(input)
    outputs = []
    for output in config_json['outputs']:
        output['type'] = 1
        outputs.append(output)
    taskFileEntityList = inputs + outputs
    pattern = '\#\{.*?\}'
    match_list = re.findall(pattern=pattern, string=taskCmd)
    for i in range(len(match_list)):
        exist = False
        for taskCmdParamEntity in taskCmdParamEntityList:
            if taskCmdParamEntity['index'] == i:
                exist = True

                if taskCmdParamEntity['type'] == 2 or taskCmdParamEntity['type'] == 3:
                    for taskFileEntity in taskFileEntityList:
                        if taskFileEntity['key'] != '' and '*' in taskFileEntity['name']:
                            myLogger.error_logger('Please fill in the exact command line input file name during the test run')

                        if taskFileEntity['key'] == taskCmdParamEntity['paramKey']:
                            if taskFileEntity['type'] == 0:
                                taskCmd = taskCmd.replace(match_list[i], taskCmdParamEntity['prefix'] + "/input/" + taskFileEntity['name'])
                            if taskFileEntity['type'] == 1:
                                taskCmd = taskCmd.replace(match_list[i], taskCmdParamEntity['prefix'] + "/output/" + taskFileEntity['name'])
                if taskCmdParamEntity['type'] == 0 or taskCmdParamEntity['type'] == 1:
                    taskCmd = taskCmd.replace(match_list[i], taskCmdParamEntity['prefix'] + taskCmdParamEntity['paramValue'])

                if taskCmdParamEntity['type'] == 4:
                    taskCmd = taskCmd.replace(match_list[i], taskCmdParamEntity['prefix'] + '/input/')

                if taskCmdParamEntity['type'] == 5:
                    taskCmd = taskCmd.replace(match_list[i], taskCmdParamEntity['prefix'] + '/output/')

        if exist == False:
            taskCmd = taskCmd.replace(match_list[i], '')

    runDocker(taskCmd=taskCmd, imageName=config_json['imageName'])
    checkOutputFile(outputs)

def getAllFiles(path):
    paths = []
    for root, dirs, files in os.walk(path):
        for file in files:
            paths.append({'dir': root, 'file': file})

    return paths

def checkOutputFile(outputFiles):
    paths = getAllFiles(os.getcwd() + '/output/')
    allFindFiles = []
    for file in outputFiles:
        if file['name'].startswith('*') == False:
            findFiles = []
            for filePath in paths:
                if filePath['file'] == file['name']:
                    findFiles.append(filePath)
                    allFindFiles.append(filePath)
            if len(findFiles) == 0:
                myLogger.error_logger('Missing output file')
            if len(findFiles) > 1:
                myLogger.error_logger('Output duplicate name file')

    for file in outputFiles:
        if file['name'].startswith('*'):
            suffix = os.path.splitext(file['name'])[1]
            findFiles = []
            for filePath in paths:
                if os.path.splitext(filePath['file'])[1] == suffix:
                    flag = 0
                    for tempFile in allFindFiles:
                        if filePath['file'] == tempFile['file']:
                            flag = 1
                    if flag == 0:
                        findFiles.append(filePath)
                        allFindFiles.append(filePath)

            if len(findFiles) == 0:
                myLogger.error_logger('Not matched to general configuration file')
            if len(findFiles) > 1:
                myLogger.error_logger('Matching to multiple pass through files')

def runDocker(taskCmd, imageName):
    client = docker.from_env()
    container = client.containers.run(image=imageName, auto_remove=True, detach=True, stdout=True, stderr=True, command=taskCmd,
                          volumes={
                              os.getcwd() + '/input/': {'bind': '/input', 'mode': 'rw'},
                              os.getcwd() + '/output/': {'bind': '/output', 'mode': 'rw'}
                          },
                          working_dir='/'
                          )
    for line in container.logs(stream=True):
        print(line)
