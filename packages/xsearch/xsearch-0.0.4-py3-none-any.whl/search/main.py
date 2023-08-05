from page import SearchPage, IndexPage
from input import SearchContent
from output import CrawledContent


if __name__ == '__main__':

    search_content = SearchContent.user_input()
    search_list = search_content.convert_to_list()
    c_content = CrawledContent.user_input()
    search_page = SearchPage.user_input()
    n = 30
    for i in range(0, len(search_list), n):
        search_page.startup()
        s_list = search_list[i:i+n]
        search_page.submit_keyword(s_list[0])
        index_page = IndexPage(search_page.driver)

        for kw in s_list:
            index_page.submit_keyword(kw)
            res = index_page.get_search_result()
            c_content.update(kw, res)
            if c_content.analyse:
                c_content.extract_tags()
            c_content.export()
        index_page.driver.quit()
    print("--------查询结束--------")
