# -*- coding: utf-8 -*-

import requests
import re
import os

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
def main():
    url = 'http://www.jingcaiyuedu.com/book/' + book_number + '.html'
    
    response = requests.get(url, headers = headers)
    response.encoding = 'utf-8'
    html = response.text
    
    #获取小说的名字
    title = re.findall(r'<meta property="og:title" content="(.*?)"/>', html)[0]
    #获取小说的类型
    book_type = re.findall(r'<meta property="og:novel:category" content="(.*?)"/>', html)[0]
    #获取小说的作者
    auther = re.findall(r'<meta property="og:novel:author" content="(.*?)"/>', html)[0]
    
    #获取每一章的地址和章节名称
    dl = re.findall(r'<dl id="list">.*?</dl>', html, re.S)[0]
    chapter_info_list = re.findall(r'href="(.*?)">(.*?)</a>', dl)
    
    #新建文件以保存小说
    with open('%s.txt' %title, 'w', encoding = 'utf-8')  as f:
        f.write('书名《%s》--作者：%s--类型：%s' %(title,auther,book_type))
        f.write('\r\n\r\n')
        for chapter_info in chapter_info_list:
            chapter_url, chapter_title = chapter_info
            chapter_url = 'http://www.jingcaiyuedu.com%s' %chapter_url
            #下载章节内容
            chapter_response = requests.get(chapter_url)
            chapter_response.encoding = 'utf-8'
            chapter_html = chapter_response.text
            #提取章节内容
            chapter_content = re.findall(r'<script>a1\(\);</script>(.*?)<script>a2\(\);</script>', chapter_html, re.S)[0]
            #处理文本内容
            chapter_content = chapter_content.replace(' ', '')
            chapter_content = chapter_content.replace('&nbsp;', '')
            chapter_content = chapter_content.replace('<br/><br/>', '\r\n')
            print(chapter_title)
            f.write(chapter_title)
            f.write('\r\n')
            f.write(chapter_content)
            f.write('\r\n\r\n')

if __name__ == '__main__':
    book_number  = input('请输入书号：')
    main()
