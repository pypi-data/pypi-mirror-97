import os
import json
import csv
import jieba.analyse
from itertools import permutations


class CrawledContent:

    def __init__(self, export_file, analyse):
        self.export_file = export_file
        self.analyse = analyse
        self.next = {}
        self.result = {}

    @classmethod
    def user_input(cls):
        while 1:
            export_file = input('请输入导出文件，支持csv/json')
            if export_file.split('.')[-1] in ['csv', 'json']:
                break

        a_list = ['', 'a', 'n', 'v'] + list(map(lambda x: ','.join(x), list(permutations(['n', 'a', 'v'], 2)) +
                                                list(permutations(['n', 'a', 'v'], 3))))
        while 1:
            analyse = input('请输入需要提取的关键词类型，如有多个用逗号分隔，如无请直接回车')
            if analyse in a_list:
                break

        return cls(
            export_file,
            analyse
        )

    def update(self, keyword, result_list):
        self.next = {keyword: result_list}
        self.result.update(self.next)

    def export(self):
        if self.export_file.split('.')[-1] == 'csv':
            with open(self.export_file, 'a', newline='', encoding='utf-8-sig') as csv_file:
                writer = csv.writer(csv_file)
                key = list(self.next.keys())[0]
                val = self.next[key]
                for i in val:
                    writer.writerow([key, val.index(i) + 1] + i)

        if self.export_file.split('.')[-1] == 'json':
            if os.path.exists(self.export_file):
                with open(self.export_file, encoding='utf-8') as json_file:
                    result_dict = json.load(json_file)
                result_dict.update(self.next)
            else:
                result_dict = self.next
            with open(self.export_file, 'w', encoding='utf-8') as json_file:
                json.dump(result_dict, json_file, ensure_ascii=False, indent=4)

    def extract_tags(self, idx=2, topK=3):
        global tags
        key = list(self.next.keys())[0]
        val = self.next[key]
        POS_dict = {'n': ('n', 'nr', 'ns', 'nt', 'nz'),
                    'a': ('a', 'ad', 'an'),
                    'v': ('v', 'vd', 'vn')}
        for k in range(len(val)):
            for p in self.analyse.split(','):
                try:
                    tags = jieba.analyse.extract_tags(val[k][idx], topK=topK, allowPOS=POS_dict.get(p))
                    tags = ' '.join(tags)
                except AttributeError:
                    tags = ' '
                finally:
                    self.next[key][k].append(tags)
