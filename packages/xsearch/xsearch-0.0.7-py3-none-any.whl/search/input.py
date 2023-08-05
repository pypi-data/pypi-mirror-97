import pandas as pd
import os
from itertools import combinations


class SearchContent:
    def __init__(self, import_file, site, filetype, sep, combine):
        filetypes = ['swf', 'pdf', 'ps', 'dwf', 'kml', 'kmz', 'gpx', 'hwp', 'htm', 'html',
                     'xls', 'xlsx', 'ppt', 'pptx', 'doc', 'docx', 'odp', 'ods', 'odt',
                     'rtf', 'svg', 'tex', 'txt', 'text', 'bas', 'c', 'cc', 'cpp', 'cxx',
                     'h', 'hpp', 'cs', 'java', 'pl', 'py', 'wml', 'wap', 'xml']
        self.import_file = import_file
        self.site = [] if site == '' else site.split(',')
        self.filetype = [] if filetype == '' else filetype.split(',')
        self.filetype = [i for i in self.filetype if i in filetypes]
        self.sep = sep
        self.combine = combine

    @classmethod
    def user_input(cls):
        while 1:
            import_file = input('请输入文件名')
            if os.path.exists(import_file) and import_file.split('.')[-1] in ['txt', 'csv', 'xlsx']:
                break
            else:
                if not os.path.exists(import_file):
                    print('！！！文件不存在！！！')
                if import_file.split('.')[-1] not in ['txt', 'csv', 'xlsx']:
                    print('！！！文件类型不符！！！')

        site = input('请输入指定站点，如有多个用逗号分隔，如无请直接回车')
        filetype = input('请输入指定文件类型，如有多个用逗号分隔，如无请直接回车')
        sep = '\n'
        combine = 1
        return cls(
            import_file,
            site,
            filetype,
            sep,
            combine
        )

    def convert_to_list(self):
        """
        :return: 待查询的字符串
        """
        if self.import_file.split('.')[-1] == 'txt':
            f = open(self.import_file, 'r', encoding='utf-8')
            keywords = f.read().strip().split(sep=self.sep)
        elif self.import_file.split('.')[-1] == 'csv':
            keywords = pd.read_csv(self.import_file, header=None).iloc[:, 0].tolist()
        elif self.import_file.split('.')[-1] == 'xlsx':
            keywords = pd.read_excel(self.import_file, header=None).iloc[:, 0].tolist()
        else:
            print('请选择正确格式文件')
            return None

        keywords = [k.strip() for k in keywords if k.strip() != '']

        if self.combine > 1:
            for i in range(2, self.combine+1):
                cl = list(map(lambda x: ' '.join(x), combinations(keywords, i)))
                keywords.extend(cl)
        if len(self.site) > 0:
            keywords = ['{} site:{}'.format(string, site_) for string in keywords for site_ in self.site]
        if len(self.filetype) > 0:
            keywords = ['{} filetype:{}'.format(string, file_) for string in keywords for file_ in self.filetype]
        return keywords
