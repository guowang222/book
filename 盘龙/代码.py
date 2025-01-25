import os
import random
import requests
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup_browser():
    """
    设置并返回浏览器驱动
    """
    return Chrome(service=Service('E:\\tools\\chrome\\chromedriver.exe'))

def content(wd):
    """
    获取当前网页的标题和正文内容
    """
    data = {}
    try:
        time.sleep(1)
        title = wd.find_element(by=By.TAG_NAME, value='h1')
        data['title'] = title.text.strip()
        text = wd.find_element(by=By.ID, value='content')
        data['text'] = text.text.strip()

        # 点击“下一章”
        link_next = wd.find_elements(by=By.CSS_SELECTOR, value="div[class='bottem1'] > a")
        link_next[2].click()
        time.sleep(1)  # 等待加载页面
        return data
    except Exception as e:
        logging.error(f"页面抓取失败: {e}")
        return None

def write_md(data, path, j):
    """
    将抓取到的数据保存为 Markdown 文件
    """
    try:
        text = data.get('text').replace('\n', '\n       ')  # 格式化文本
        file_path = os.path.join(path, f'{str(j)}_{data.get("title")}.md')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # 确保目录存在

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f'# {data.get("title")}\n        {text}')
        logging.info(f"成功写入文件: {file_path}")
    except Exception as e:
        logging.error(f"写入文件失败: {e}")

def get_next_chapter_title(wd):
    """
    获取当前章节的标题，用于判断是否已经到达目标章节
    """
    try:
        return wd.find_element(by=By.TAG_NAME, value='h1').text.strip()
    except Exception as e:
        logging.error(f"获取标题失败: {e}")
        return None

def main(url, file_path, start_chapter):
    """
    主程序逻辑函数
    """
    # 初始化浏览器
    wd = setup_browser()
    # 打开网页
    wd.get(url)

    j = start_chapter  # 从指定章节开始
    failed_pages = []  # 用于记录失败的页面

    while True:
        try:
            # 获取当前章节的标题
            chapter_title = get_next_chapter_title(wd)

            if chapter_title == '第二十一集 巅峰 第四十三章 新的名字（大结局）（下）':
                break  # 如果到达目标章节，结束爬取

            logging.info(f"正在处理: {chapter_title}")
            data = content(wd)  # 获取页面内容

            if data:
                write_md(data, file_path, j)  # 写入文件
                j += 1
            else:
                failed_pages.append(f"第 {j} 页 - {chapter_title}")  # 记录失败的页面

        except Exception as e:
            failed_pages.append(f"第 {j} 页 - 异常错误: {e}")  # 捕获任何未处理的异常并记录失败
            logging.error(f"异常发生: {e}")
            j += 1

        # 延时控制，模拟正常的访问间隔
        sleep_time = random.uniform(0.5, 1)
        time.sleep(sleep_time)

    # 输出失败的页面列表
    logging.info(f"处理完成，失败的页面: {failed_pages}")

    # 关闭浏览器
    wd.quit()

if __name__ == '__main__':
    # 示例调用
    url = 'https://www.beqege.cc/16631/221741.html'  # 起始章节 URL
    file_path = 'F:\\代码库\\爬虫\\盘龙'  # 文件写入路径
    start_chapter = 1  # 从第1章开始

    main(url, file_path, start_chapter)
