import os
import re
import requests
from lxml import etree


strat_url = 'https://www.plmm.com.cn/xinggan/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/78.0.3904.87 Safari/537.36'}


def parser(target_url):
    raw_html = requests.get(target_url, headers=headers)
    if raw_html.status_code != 200:
        print('访问出错')
    html = etree.HTML(raw_html.content)
    return html


def get_main_page(url):
    main_page = parser(url)
    titles = main_page.xpath('//span[@class="absolute block align-center ellipsis pic-bone-imgname-list"]/h3/a/text()')
    inner_pages = main_page.xpath('//span[@class="absolute block align-center ellipsis pic-bone-imgname-list"]/h3/a/@href')
    for title, inner_page in zip(titles, inner_pages):
        inner_page = re.sub('//', 'https://', inner_page)
        downloader(title, inner_page)
    turn_page(main_page)


def turn_page(target):
    turn_bottom = target.xpath('//span[@id="npage"]/a/@href')
    if turn_bottom is not None:
        for turn in turn_bottom:
            new_html = 'https://www.plmm.com.cn' + turn
            get_main_page(new_html)


def downloader(title, page):
    inner = parser(page)
    imgs = inner.xpath('//ul[@class="grid effect-1"]//a/@href')
    try:
        print('准备开始下载')
        if not os.path.exists('images\\' + title):
            print('创建文件夹' + title)
            os.makedirs('images\\' + title)
        i = 0
        for img in imgs:
            i += 1
            img = str(re.sub('//', 'https://', img))
            img = re.sub('@!w1200', '', img)
            filename = 'images\\{}\\'.format(title) + str(i) + '.jpg'
            if not os.path.exists(filename):
                print('正在下载第' + str(i) + '张图片，地址：' + img)
                r = requests.get(img, headers=headers)
                with open(filename, 'wb+') as f:
                    f.write(r.content)
    except Exception as ex:
        print('下载出错.{}'.format(ex))


if __name__ == '__main__':
    get_main_page(strat_url)
