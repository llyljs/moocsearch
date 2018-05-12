from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
from time import clock


#exclude courses from edX
def selector(tag:Tag):
    return  tag.name=='div' and tag.attrs.get('class') is not None and 'coursename' in tag.attrs['class'] and 'edX' not in tag.get_text()
def search(keywords:str):
    search_base_url = 'http://www.xuetangx.com/courses/search?query={}&qt=1&page={}'
    header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
    current_page = 1
    response = requests.get(search_base_url.format(keywords,current_page),headers=header)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    footer = soup.body.find('div',id='list_pager')
    page_count = int(footer['data-pagecount'])
    xuetangx_List = []

    while True:
        course_block = soup.body.find_all(selector)
        if len(course_block) > 0:
            try:
                Title = map(lambda x:x.a.get_text(strip=True),course_block)
                Link =  map(lambda x:x.a['href'],course_block)
                School = map(lambda x:x.find('div',class_='fl name').ul.li.get_text(strip=True),course_block)
                for i,j,k in zip(Title,Link,School):
                    xuetangx_List.append({'Title':i,'Link':'http://www.xuetangx.com'+j,'School':k})
                #for speed reason, just get 1 page
                break
            except:
                pass
        if current_page<page_count:
            current_page += 1
        else:
            break

        response = requests.get(search_base_url.format(keywords, current_page), headers=header)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
    return xuetangx_List

if __name__ == '__main__':
    start = clock()
    search('病理学')
    end = clock()
    print(end-start)