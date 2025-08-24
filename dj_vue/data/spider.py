import requests
import pandas as pd

table = pd.read_excel("终 地点2.xlsx")
def get_location(address, api_key):
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "address": address,
        "key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data["status"] == "1" and data["count"] != "0":
        location = data["geocodes"][0]["location"]
        return tuple(map(float, location.split(',')))
    else:
        return None

# 替换为你自己的API密钥
api_key = "d881f37a605d92c23712c72ef139114d"
for i,row in table.iterrows():
    # 地点名称
    address = row['地点']
    # 获取地点的经纬度
    location = get_location(address, api_key)
    if location:
        print("经度:", location[0])
        print("纬度:", location[1])
        with open("address.csv","a+",encoding="utf-8") as f:
            f.write(f"{address},{location[0]},{location[1]}\n")
