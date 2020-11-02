import os
import json

if __name__ == "__main__":
    dirs = os.listdir("data/json")
    dirs.sort()
    current_id = ""
    current_json_content = {}
    for dir in dirs:
        id = dir[6:22]
        if(current_id == ""):
            file = open("data/json/" + dir,'r')
            current_json_content = json.load(file)
            current_id = id
            file.close()
            continue
        if(current_id != id):
            file = open('data/final_jsons/weibo_final_%s.json' % id,'w')
            json.dump(current_json_content,file,indent = 6)
            current_json_content = {}
            current_id = ""
            file.close()
            continue
        temp_content = json.load(open("data/json/" + dir,'r'))
        current_json_content["data"]["data"].extend(temp_content["data"]["data"])