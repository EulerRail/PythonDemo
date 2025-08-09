import json
import requests
import os
import shutil
import sys
import data_fetcher

"""
File Language: Python
Comment Language: 中文
Description: 角色数据处理与命令行交互
"""

# 全局变量，存储所有角色数据
character_data = {"character": {"basic_info": []}}
 # 单个角色的基础信息模板
character_basic_template = {
    "id": 0,
    "name": "",
    "star": 0,
    "fate": "",
    "element": ""
}

def extract_character_list(json_data):
    """
    从原始json数据中提取角色列表
    参数: json_data (dict)
    返回: 角色列表 (list)
    """
    return json_data["data"]["list"][0]["children"][0]["list"]

def build_character_basic_info(template, character_id, name, star, fate, element):
    """
    构造单个角色的基础信息字典
    """
    info = template.copy()
    info["id"] = character_id
    info["name"] = name
    info["star"] = star
    info["fate"] = fate
    info["element"] = element
    return info

def load_character_data():
    """
    从data.json导入角色数据,下载图片并保存基础信息到mydata.json
    """
    global character_data
    global character_basic_template
    if os.path.exists("data/picture"):
        shutil.rmtree("data/picture")
    os.mkdir("data/picture")
    if not os.path.exists("data/json/data.json"):
        print("data文件不存在,自动爬取")
        data_fetcher.update_data()
    with open("data/json/data.json", "r", encoding="utf-8") as file:
        all_data = json.load(file)
    character_data["character"]["basic_info"] = []
    for index, item in enumerate(extract_character_list(all_data)):
        temp = character_basic_template.copy()
        ext_info = json.loads(item["ext"])["c_18"]
        text_info = ext_info["filter"]["text"]
        image_url = ext_info["picture"]["list"][0]
        # 提取fate和element
        n1 = text_info.find("命途")
        fate = text_info[n1 + 3:n1 + 3 + 2]
        n1 = text_info.find("属性")
        element = text_info[n1 + 3:n1 + 3 + 2]
        # 提取星级
        n1 = text_info.find("星级")
        star_text = text_info[n1 + 3:n1 + 3 + 2]
        star = 4 if star_text == "四星" else 5
        # 下载角色图片
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(f"data/picture/{index}.png", "wb") as img_file:
                img_file.write(response.content)
            print(f"{item['title']}图片获取成功, id: {item['content_id']}, index: {index}")
        else:
            print(f"{item['title']}图片获取异常, id: {item['content_id']}, index: {index}")
        # 添加角色基础信息
        character_data["character"]["basic_info"].append(
            build_character_basic_info(temp, index, item["title"], star, fate, element)
        )
    # 保存所有角色基础信息到mydata.json
    with open("data/json/mydata.json", "w", encoding="utf-8") as out_file:
        json.dump(character_data, out_file, ensure_ascii=False, indent=4)
    print("角色基础信息输出完毕")

def add_character():
    """
    命令行添加新角色到mydata.json
    """
    if not os.path.exists("data/json/mydata.json"):
        print("尚未导入角色数据,请先导入数据")
        return
    try:
        character_id = int(input("请输入角色ID: "))
        name = input("请输入角色名称: ")
        star = int(input("请输入角色星级(4或5): "))
        fate = input("请输入角色命途: ")
        element = input("请输入角色属性: ")
        with open("data/json/mydata.json", "r", encoding="utf-8") as file:
            temp_data = json.load(file)
        for character in temp_data["character"]["basic_info"]:
            if character["id"] == character_id:
                print("角色ID已存在,请勿重复添加")
                return
        temp_data["character"]["basic_info"].append(
            build_character_basic_info(character_basic_template, character_id, name, star, fate, element)
        )
        print(f"添加角色: {name}, ID: {character_id}, 星级: {star}, 命途: {fate}, 属性: {element}____请手动添加{character_id}.png")
        with open("data/json/mydata.json", "w", encoding="utf-8") as file:
            json.dump(temp_data, file, ensure_ascii=False, indent=4)
    except ValueError:
        print("输入无效,请重新输入")

def delete_character():
    """
    命令行删除角色
    """
    if not os.path.exists("data/json/mydata.json"):
        print("尚未导入角色数据,请先导入数据")
        return
    try:
        character_id = int(input("请输入角色ID: "))
        with open("data/json/mydata.json", "r", encoding="utf-8") as file:
            temp_data = json.load(file)
        found = False
        for character in temp_data["character"]["basic_info"]:
            if character["id"] == character_id:
                temp_data["character"]["basic_info"].remove(character)
                print(f"删除角色: {character['name']}, ID: {character_id}")
                found = True
                break
        if found:
            with open("data/json/mydata.json", "w", encoding="utf-8") as file:
                json.dump(temp_data, file, ensure_ascii=False, indent=4)
        else:
            print(f"未找到ID为{character_id}的角色")
    except ValueError:
        print("输入无效,请重新输入")

def update_data():
    """
    下载最新角色数据
    """
    data_fetcher.update_data()

def main_menu():
    """
    主交互函数,命令行菜单
    """
    while True:
        choice = input("""
请输入角色操作:
1: 从data.json导入数据(导入图片)
2: 录入新角色
3: 删除角色
4: 下载最新角色数据
5: 退出
""")
        if choice == "1":
            load_character_data()
        elif choice == "2":
            add_character()
        elif choice == "3":
            delete_character()
        elif choice == "4":
            update_data()
        elif choice == "5":
            sys.exit()
        else:
            print("无效选项,请重新输入")

# 程序入口
if __name__ == "__main__":
    main_menu()
