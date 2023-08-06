import os
import json
import csv
import jieba.analyse


class CrawledContent:

    def __init__(self, analyse, export_file):
        self.analyse = analyse
        self.export_file = export_file
        self.next = {}
        self.result = {}

    @classmethod
    def user_input(cls):
        while 1:
            try:
                analyse = int(input('需要文本分析提取关键词则键入1，否则键入0'))
                break
            except ValueError:
                print("请重新输入")
        while 1:
            export_file = input('请输入导出文件，支持csv/json')
            if export_file.split('.')[-1] in ['csv', 'json']:
                break
        return cls(
            analyse,
            export_file
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

    def extract_tags(self, idx=-1, topK=5, allowPOS=('n', 'nr', 'ns')):
        key = list(self.next.keys())[0]
        val = self.next[key]
        for k in range(len(val)):
            try:
                tags = jieba.analyse.extract_tags(val[k][idx], topK=topK, allowPOS=allowPOS)
                self.next[key][k].append(' '.join(tags))
            except AttributeError:
                pass
