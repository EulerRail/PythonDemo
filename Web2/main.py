import json
from flask import Flask, render_template, abort, send_from_directory
import os

"""
文件语言：Python
注释语言：中文
"""
# Create Flask application instance
application = Flask(__name__)

 # 加载角色列表数据
def load_character_list():
    """
    从本地JSON文件读取所有角色的基础信息列表。
    返回: 角色基础信息列表 (list of dict)
    """
    with open('data/json/mydata.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data['character']['basic_info']

 # 首页路由: 角色列表展示
@application.route("/")
def show_character_list():
    """
    渲染角色列表页面, 将所有角色信息传递给模板。
    """
    character_list = load_character_list()
    return render_template("character_list.html", character_list=character_list)

 # 角色详情页路由
@application.route("/character/<int:character_id>")
def show_character_detail(character_id):
    """
    根据角色ID查找角色详情, 渲染详情页面。
    参数: character_id (int)
    """
    character_list = load_character_list()
    character = next((c for c in character_list if c['id'] == character_id), None)
    if not character:
        abort(404)  # 未找到角色则返回404页面
    return render_template("character_detail.html", character=character)

 # 图片访问路由: 用于访问data/picture下的图片资源
@application.route("/image/<filename>")
def serve_image(filename):
    """
    根据文件名返回图片资源。
    参数: filename (str)
    """
    return send_from_directory(os.path.join("data", "picture"), filename)

 # 程序入口
if __name__ == "__main__":
    # 启动Flask开发服务器, debug模式方便调试
    application.run(port =5000,debug=True)