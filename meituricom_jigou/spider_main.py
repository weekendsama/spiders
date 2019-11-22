import os
import re
import requests
from lxml import etree


start_url = 'https://www.meituri.com/jigou/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/78.0.3904.87 Safari/537.36'}
i = 0


def parser(url):
    raw_url = requests.get(url, headers=headers)
    if raw_url.status_code != 200:
        print('解析错误:{}'.format(raw_url.status_code))
    return etree.HTML(raw_url.content)


def get_catagory(url):
    catagory = parser(url)
    names = catagory.xpath('//div[@class="jigou"]//li/a/text()')
    cata_urls = catagory.xpath('//div[@class="jigou"]//li/a/@href')
    for name, data_url in zip(names, cata_urls):
        if not os.path.exists('images\\' + name):
            print('正在创建目录 ' + name)
            os.makedirs('images\\' + name)
        get_url(name, data_url)


def get_url(title, url):
    global i
    target = parser(url)
    urls = target.xpath('//p[@class="biaoti"]/a/@href')
    names = target.xpath('//p[@class="biaoti"]/a/text()')
    for target_url, name in zip(urls, names):
        print('开始下载' + name)
        while True:
            downloader(target_url, name, title)
            target_url = next_page(target_url)
            if target_url == next_page(target_url):
                if target_url is not None:
                    downloader(target_url, name, title)
                i = 0
                break
    if url != next_page(url) or url is not None or next_page(url) is not None or next_page(url) is not 'javascript:void':
        new_url = 'https://www.meituri.com{}'.format(next_page(url))
        print('NEW URL' + new_url)
        if new_url != 'https://www.meituri.comNone' and new_url != 'https://www.meituri.comjavascript:void(0)':
            get_url(title, new_url)


def downloader(url, name, title):
    global i
    new_download_page = parser(url)
    download_links = new_download_page.xpath('/html/body/div[4]//img/@src')
    for download_link in download_links:
        try:
            i += 1
            if not os.path.exists('images\\{}\\'.format(title) + name):
                print('正在创建分集' + name)
                os.makedirs('images\\{}\\'.format(title) + name)
            filename = 'images\\{}\\{}\\'.format(title, name) + str(i) + '.jpg'
            if not os.path.exists(filename):
                print('正在下载第' + str(i) + '张图片，地址：' + download_link)
                download = requests.get(download_link, headers=headers)
                with open(filename, 'wb') as f:
                    f.write(download.content)
        except Exception as EX:
            print('下载错误{}'.format(EX))


def next_page(url):
    if url is not None:
        next_pages = parser(url)
        next_pager = next_pages.xpath('//*[@id="pages"]/a[last()]/@href')
        for the_page in next_pager:
            return the_page
    else:
        print('URL为空')


if __name__ == '__main__':
    get_catagory(start_url)