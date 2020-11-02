import json

if __name__ == "__main__":
    id = "4462638756717942"
    json_data = json.load(open("data/hot.json",'r'))
    count = 0
    for data in json_data:
        if data["id"] == id:
            print(count)
            break
        count += 1