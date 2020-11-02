import json
from json.decoder import JSONDecodeError
import requests
from clickhouse_driver import Client
from tqdm import tqdm
import time

def weibo_to_clickhouse(clickhouse_client,data,is_retweeted):
    sql = "insert into cascade (create_at,id,bid,mid,text,source,user_id,reposts_count,comments_count,attitudes_count,pending_approval_count,retweet_id,repost_type) values ('%s',%d,'%s',%d,'%s','%s',%d,%d,%d,%d,%d,%d,%d);" % (
        data["created_at"],int(data["id"]),data["bid"],int(data["mid"]),data["text"].replace('\'','\\\''),data["source"],data["user"]["id"],data["reposts_count"],data["comments_count"],data["attitudes_count"],data["pending_approval_count"],int(data["retweeted_status"]["id"]) if is_retweeted else 0,data["repost_type"] if is_retweeted else 0)
    clickhouse_client.execute(sql)

def user_to_clickhouse(clickhouse_client,data):
    sql = "insert into cascade_user (id,screen_name,description,gender,urank,followers_count,follow_count) values (%d,'%s','%s','%s',%d,%d,%d)" % (
        data["id"],data["screen_name"],data["description"],data["gender"],data["urank"],data["followers_count"],data["follow_count"])
    clickhouse_client.execute(sql)

def crawl(clickhouse_client,hot):

    last_time_weibo_count = 115
    last_time_page_count = 0


    started = False

    weibo_count = 0
    all_count = len(hot)
    for weibo in hot:
        if(weibo_count < last_time_weibo_count):
            weibo_count += 1
            continue
        id = weibo["id"]
        count = 1
        while(True):
            if((not started) and (count < last_time_page_count)):
                count += 1
                continue
            started = True
            url = "https://m.weibo.cn/api/statuses/repostTimeline?id=%s&page=%d" % (id,count)
            content = requests.get(url)
            json_data = []
            try:
                json_data = json.loads(content.content)
            except JSONDecodeError:
                # count += 1
                print("error when decode json, id: %s, page: %d" % (id,count))
                print("retry after one minute.")
                time.sleep(60)
                continue
            if(json_data["ok"] == 0):
                print("json is not ok")
                break
            file_name = "data/json/weibo_%s_page_%d.json" % (id,count)
            file = open(file_name,'w')
            json.dump(json_data,file,indent=4,ensure_ascii=False)
            file.close()
            print("complete page %d of id: %s" % (count,id))
            count += 1
        print("complete id: %s, %d/%d" % (id,weibo_count,all_count))
        weibo_count += 1
        

if __name__ == "__main__":
    f = open("data/hot.json",'r')
    hot_json = json.load(f)
    client = Client(host='121.43.42.31',port='4118',user="default" ,password="123",database = "weibo")
    crawl(client,hot_json)
