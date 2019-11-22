import os
import re
import requests
from lxml import etree


start_url = 'http://www.quanshuwang.com/list/1_1.html'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/78.0.3904.87 Safari/537.36'}


def parser(url):
        raw_url = requests.get(url, headers=headers)
        if raw_url.status_code != 200:
            print('解析错误:{},正在重试'.format(raw_url.status_code))
            parser(url)
        return etree.HTML(raw_url.content)


def get_novel_lists(url):
    if url is not None:
        target = parser(url)
        if target is not None:
            novel_names = target.xpath('//span[@class="l"]/a[1]/@title')
            novel_pages = target.xpath('//span[@class="l"]/a[1]/@href')
            for novel_name, novel_page in zip(novel_names, novel_pages):
                print('开始下载小说:' + novel_name)
                downloader(novel_name, novel_page)
            if turn_page(url) is not None:
                new_page = turn_page(url)
                get_novel_lists(new_page)


def turn_page(url):
    raw_url = parser(url)
    pagers = raw_url.xpath('//div[@class="pagelink"]/a[@class="next"]/@href')
    for pager in pagers:
        return pager


def downloader(name, page):
    raw_content = parser(page)
    if raw_content is not None:
        real_contents = raw_content.xpath('//div[@class="b-oper"]/a[1]/@href')
        for real_content in real_contents:
            content = parser(real_content)
            if content is not None:
                indexs = content.xpath('//div[@class="clearfix dirconone"]//li/a/text()')
                targets = content.xpath('//div[@class="clearfix dirconone"]//li/a/@href')
                for index, target in zip(indexs, targets):
                    try:
                        if not os.path.exists('novels\\{}'.format(name)):
                            print('正在创建文件夹:' + name)
                            os.makedirs('novels\\{}'.format(name))
                        filename = 'novels\\{}\\'.format(name) + index + '.txt'
                        if not os.path.exists(filename):
                            print('正在下载：' + index + '地址：' + target)
                            download = parser(target)
                            if download is not None:
                                download_texts = download.xpath('//div[@class="mainContenr"]/text()')
                                for download_text in download_texts:
                                    with open(filename, 'ab')as f:
                                        f.write(download_text.encode('utf-8'))
                    except Exception as EX:
                        print('下载出错：{}'.format(EX))


if __name__ == '__main__':
    get_novel_lists(start_url)