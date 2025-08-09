# data_fetcher.py
# 用于从API获取最新角色数据
import json
import requests

def update_data():
    """
    从米哈游API获取最新角色数据,并保存到本地 data.json 文件
    """
    api_url = "https://act-api-takumi-static.mihoyo.com/common/blackboard/sr_wiki/v1/home/content/list?app_sn=sr_wiki&channel_id=17"
    response = requests.get(api_url)
    if response.status_code == 200:
        json_data = response.json()
        print("角色数据获取成功")
    else:
        print(f"从 {api_url} 获取角色数据失败")
        raise SystemExit
    with open("data/json/data.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(json_data, ensure_ascii=False, indent=4))
        print("角色数据文件已更新")

if __name__ == "__main__":
    update_data()
