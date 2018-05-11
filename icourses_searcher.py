from bs4 import BeautifulSoup
import requests

def search(keywords:str, curPage:int=1):
    search_url = 'http://www.icourses.cn/web//sword/portalsearch/searchPage'
    header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
    data = {'kw':keywords,'curPage':curPage}
    response = requests.post(search_url,data=data,headers=header)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text,'lxml')
    Atitle = soup.body.find_all('a',class_='icourse-desc-title')
    School = soup.body.find_all('span',class_='icourse-desc-school')
    icourses_List = []
    icourse163_List = []
    for i in range(len(Atitle)):
        Link:str = Atitle[i]['href']
        if 'icourse163' in Link:
            course = {'Title': Atitle[i].get_text(), 'Link': Atitle[i]['href'], 'School': School[i].get_text()}
            icourse163_List.append(course)
        elif 'icourses' in Link:
            course = {'Title':Atitle[i].get_text(),'Link':Atitle[i]['href'],'School':School[i].get_text()}
            icourses_List.append(course)
    return (icourse163_List,icourses_List)
if __name__ == '__main__':
    search('python')