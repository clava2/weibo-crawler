from clickhouse_driver import Client
import json

if __name__ == "__main__":
    client = Client(host='121.43.42.31',port='4118',user="default" ,password="123",database = "weibo")
    sql = "select id,bid,created_at,reposts_count from weibo where reposts_count > 350 and reposts_count < 2000 and created_at > '2020-01-01 00:00:00' order by created_at;"
    result = client.execute(sql)
    result = [{"id":r[0],"bid":r[1],"publish-time":str(r[2]),"retweet-count":r[3]} for r in result]
    file = open("data/hot.json",'w')
    json.dump(result,file)
    file.close()
    print(len(result))