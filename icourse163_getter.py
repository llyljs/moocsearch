import requests
import time
import re


class icourse163_getter:
    def __init__(self, id):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'}
        self.base_url = 'https://www.icourse163.org/course/{}'
        self.id = id

    def get_file_url(self, lesson_content_id, content_type, lesson_id):
        post_data = {'callCount': '1', 'scriptSessionId': '${scriptSessionId}190',
                     'httpSessionId': '5531d06316b34b9486a6891710115ebc', 'c0-scriptName': 'CourseBean',
                     'c0-methodName': 'getLessonUnitLearnVo', 'c0-id': '0', 'c0-param0': 'number:' + lesson_content_id,
                     'c0-param1': 'number:' + content_type, 'c0-param2': 'number:0', 'c0-param3': 'number:' + lesson_id,
                     'batchId': str(int(time.time() * 1000))}
        r = requests.post('https://www.icourse163.org/dwr/call/plaincall/CourseBean.getLessonUnitLearnVo.dwr',
                              data=post_data,headers=self.header)
        if content_type == '1':
            mp4_url = (re.search(r'mp4ShdUrl="(.*?\.mp4.*?)"', r.text) or re.search(r'mp4HdUrl="(.*?\.mp4.*?)"',
                                                                                    r.text) or re.search(
                r'mp4SdUrl="(.*?\.mp4.*?)"', r.text)).group(1)
            return mp4_url
        elif content_type == '3':
            pdf_url = re.search(r'textOrigUrl:"(.*?)"', r.text).group(1)
            return pdf_url

    def get_chapters(self):
        url = self.base_url.format(self.id)
        r = requests.get(url,headers=self.header)
        term_id = re.search(r'termId : "(\d+)"', r.text).group(1)
        post_data = {'callCount': '1', 'scriptSessionId': '${scriptSessionId}190', 'c0-scriptName': 'CourseBean',
                     'c0-methodName': 'getMocTermDto', 'c0-id': '0', 'c0-param0': 'number:' + term_id,
                     'c0-param1': 'number:1', 'c0-param2': 'boolean:true', 'batchId': str(int(time.time() * 1000))}
        r = requests.post('https://www.icourse163.org/dwr/call/plaincall/CourseBean.getMocTermDto.dwr',
                              data=post_data,headers= self.header)

        all = r.text.encode('utf-8').decode('unicode_escape')

        chapters_raw = re.findall(r'homeworks=\w+;.+id=(\d+).+name="(.+)";', all)
        List_chapter = []
        for chapter_ID, chapter_title in chapters_raw:
            section_raw = re.findall('chapterId=' + chapter_ID + r'.+contentType=1.+id=(\d+).+name="(.+)".+test', all)
            List_section = []
            # drop chapters that don't contain section
            if section_raw:
                for section_id, section_title in section_raw:
                    List_lesson = []
                    lessons_raw = re.findall(
                        r'contentId=(\d+).+contentType=(\d).+id=(\d+).+lessonId=' + section_id + r'.+name="(.+)"', all)
                    # drop section that don't contain lesson
                    if lessons_raw:
                        for lesson_content_id, content_type, lesson_id, lesson_title in lessons_raw:
                            if content_type == '1' or content_type == '3':
                                url = self.get_file_url(lesson_content_id, content_type, lesson_id)
                                List_lesson.append({'file_name': lesson_title, 'file_url': url,
                                                    'file_type': 'pdf' if content_type == '3' else 'mp4'})
                        List_section.append({'section_title': section_title, 'files': List_lesson})
                if List_section:
                    List_chapter.append({'chapter_title': chapter_title, 'chapter_content': List_section})
        return List_chapter

if __name__ == '__main__':
    print(icourse163_getter('BIT-1001870001').get_chapters())
