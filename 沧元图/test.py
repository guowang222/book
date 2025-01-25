import os
import random
import requests
from lxml import etree
from time import sleep
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 请求头
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br, zstd',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'cookie': 'cf_clearance=wYP4_27N9oKD_P1XzelnyzybQYEu5xp2L4WEwZWqy3Q-1737653928-1.2.1.1-H7fbAygDniLWYP6k2wX3CBErcI3HSmNvF9of77RwmomfC8.J4FTIg0RybjaZwQGzpGiP_RJy3fQsw4Zz8Oq_EOUOGfIt5_PT95asqzi0OGeQ.8s7zz_1xMorqEOJ7MTGGcRrHU1y8PZPWrmdsCUifkiKWh4YLq1vx3w5BXtWrXWxFdPY6AF__YXSLSublRcfS8lUKAmi9nwuoPGi.5chztS9hwPK_BjbfdRA5TKIiSFvKivOmpZ.gVDANgeypGAKo0j5R_PkPcSw0m.hz5WBCQ4EN9n7hJUTC4oXK7N6XLU',  # 请替换为你自己的 cookie
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0'
}

# 创建请求会话
session = requests.Session()
session.headers.update(headers)

# 获取章节内容的函数
def get_center(url):
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()  # 如果响应状态码不是 200，将抛出异常
        parser = response.text
        tree = etree.HTML(parser)
        name = tree.xpath('//h1/text()')[0].strip()  # 获取标题并去除首尾空格
        content = tree.xpath('//div[@id="content"]//p/text()')
        return name, content
    except requests.exceptions.RequestException as e:
        logging.error(f"请求错误: {url}, 错误信息: {e}")
        return None, None

# 写入 Markdown 文件的函数
def write_md(data, name, j):
    text = '\n\n'.join(data)
    try:
        # 动态生成文件路径
        file_path = os.path.join('F:', '代码库', '爬虫', '沧元图', f'{j}_{name}.md')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)  # 确保目录存在
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f'# {name}\n\n{text}')
        logging.info(f"成功写入文件: {file_path}")
    except Exception as e:
        logging.error(f"写入文件失败: {e}")

# 主程序逻辑
j = 1
err_list = []
for i in range(1, 768):
    url = f'https://www.beqege.cc/15702/20936{i}.html'
    logging.info(f"正在处理: {url}")
    name, content = get_center(url)
    if name and content:
        write_md(content, name, j)
    else:
        logging.error(f"第 {i} 页处理失败")
        err_list.append(i)
    j += 1
    sleep_time = random.uniform(3, 6)  # 随机设置请求间隔（3到6秒）
    logging.info(f"休眠 {sleep_time} 秒")
    sleep(sleep_time)

logging.info(f"处理完成，失败的页码: {err_list}")
