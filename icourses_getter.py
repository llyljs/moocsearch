import requests
from bs4 import BeautifulSoup
class icourses_getter:
    def __init__(self,id):
        self.base_url = 'http://www.icourses.cn/web/sword/portal/{}?cid={}'
        self.id= id
        self.header= {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36','Accept-Encoding':'gzip, deflate'}

    def get_chapter(self):
        def selector(chapter):
            chapter_title = chapter.find('a', class_='chapter-title-text').get_text().replace('\n',' ').replace('\t','')
            files_raw = chapter.find_all('a', class_='chapter-body-content-text-in')
            files = list(map(lambda file: {'file_name': file.attrs['data-title'], 'file_type': file.attrs['data-type'],
                                           'file_url': file.attrs['data-url']}, files_raw))
            return {'chapter_title': chapter_title, 'files': files}
        url = self.base_url.format('shareChapter',self.id)
        try:
            r = requests.get(url,headers = self.header)
        except:
            return
        soup = BeautifulSoup(r.text,'lxml')
        chapters_raw = soup.find_all('li',class_='panel ')
        chapters = list(map(selector,chapters_raw))
        return chapters

if __name__ == '__main__':
    getter = icourses_getter('7259')
    chapters = getter.get_chapter()
    print(chapters)