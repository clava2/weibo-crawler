import json
import os

if __name__ == '__main__':
    dirs = os.listdir("data/final_jsons")
    for dir in dirs:
        print(dir)
        id = dir[12:30]
        filename = "data/final_jsons/" + dir
        file = open(filename,'r')
        json_content = json.load(file)
        for data in json_content["data"]["data"]:
            print(data)
            id = data["id"]
            user = data["user"]["id"]
            src_user = data["retweeted_status"]["user"]["id"]
