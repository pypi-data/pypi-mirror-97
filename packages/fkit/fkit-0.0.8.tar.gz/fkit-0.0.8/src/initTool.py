import os, json

template = """{
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
}"""


def initTool(name):

    str = template.replace("\"name\": \"\",", "\"name\": \"" + name.strip() + "\",");
    cur_path = os.getcwd()
    print(template)
    with open(cur_path + '/tool.py', 'w', encoding="utf-8") as f:
        f.write(str)
    os.mkdir(os.getcwd() + '/input')
    os.mkdir(os.getcwd() + '/output')
