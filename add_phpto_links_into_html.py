import json
from bs4 import BeautifulSoup
import os

def update_photo_gallery(json_file, html_file):
    """
    从JSON文件读取照片链接并更新到HTML页面中指定的<div id="photos_here">，移除原有内容并插入新的图片元素
    """
    # 检查 HTML 文件是否存在
    if not os.path.exists(html_file):
        print(f"错误：HTML文件 {html_file} 不存在")
        return

    # 读取 JSON 中的图片链接
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        photo_links = data.get('main_page', [])
        if not photo_links:
            print("JSON文件中未找到照片链接")
            return
    except Exception as e:
        print(f"读取JSON文件时出错: {e}")
        return

    # 解析 HTML 文件
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
    except Exception as e:
        print(f"读取HTML文件时出错: {e}")
        return

    # 找到目标 div
    target_div = soup.find(id="photos_here")
    if not target_div:
        print("未找到 id='photos_here' 的 div")
        return

    # 清空原内容
    target_div.clear()

    # 添加新的图片元素
    for img_url in photo_links:
        photo_html = soup.new_tag("div", attrs={
            "class": "flex w-full p-1 md:w-1/2 flex-wrap overflow-hidden"
        })

        a_tag = soup.new_tag("a", href=img_url)
        a_tag.attrs["data-fancybox"] = "gallery"

        img_tag = soup.new_tag("img", src=img_url)
        img_tag.attrs["class"] = (
            "block w-full object-cover object-center aspect-[3/2] "
            "opacity-0 animate-fade-in transition duration-500 "
            "transform scale-100 hover:scale-105"
        )

        # 组合标签结构
        a_tag.append(img_tag)
        photo_html.append(a_tag)
        target_div.append(photo_html)

    # 保存更新后的 HTML
    try:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f"✅ 成功更新 {html_file}，共添加 {len(photo_links)} 张照片")
    except Exception as e:
        print(f"保存HTML文件时出错: {e}")

if __name__ == "__main__":
    # 配置路径（请根据实际情况调整）
    json_file = "./photos.json"
    html_file = "./index.html"

    update_photo_gallery(json_file, html_file)
