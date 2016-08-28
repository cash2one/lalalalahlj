# -*- coding: utf-8 -*-#
# filename:pager.py
# __author__ = 'wanglina'


class pager(object):
    _pagebar_html = "%s"

    def __init__(self, url, page, count, perpage):
        self._url = url
        self._page = page
        self._count = control_page_num(count, perpage)
        count = control_page_num(count, perpage)
        self._perpage = perpage
        self._pagenum = (count / perpage + 1) if count % perpage > 0 else (
        count / perpage if count / perpage > 0 else 1)
        self.pagebar = ""

    def show_page(self):
        self.pagebar = ''
        if self._page == 1:
            self.pagebar += '<span class="disabled">&lt; </span><span class="current">' + u"首页" + '</li></span>'
            self.pagebar += '<a href="#">' + u"上一页" + '</a>'
        else:
            self.pagebar += '<a href="' + self._url + '_1.html' + '">' + u"首页" + '</a>'
            self.pagebar += '<a href="' + self._url + '_' + str(self._page - 1) + '.html">' + u"上一页" + '</a>'

        if self._pagenum == 1:
            self.pagebar += '<span class="current">1</span>'
        else:
            if self._pagenum <= 10:
                self.dispose_url(1, self._pagenum + 1)
            else:
                if self._pagenum - self._page <= 5:
                    self.dispose_url(self._pagenum - 10, self._pagenum + 1)
                else:
                    if self._page > 4:
                        show_start = self._page - 4
                    else:
                        show_start = 1
                    self.dispose_url(show_start, show_start + 10)

        if self._page == self._pagenum:
            self.pagebar += '<a href="#">' + u"下一页" + '</a>'
            self.pagebar += '<a href="#">' + u"末页" + '</a>'
        else:
            self.pagebar += '<a href="' + self._url + '_' + str(self._page + 1) + '.html">' + u"下一页" + '</a>'
            self.pagebar += '<a href="' + self._url + '_' + str(self._pagenum) + '.html">' + u"末页" + '</a>'

        self._pagebar_html = self._pagebar_html % self.pagebar
        return self._pagenum, self._pagebar_html

    # 处理分页链接以及显示
    def dispose_url(self, start, end):
        for i in range(start, end):
            if i == self._page:
                self.pagebar += '<span class="current">' + str(i) + '</span>'
            else:
                self.pagebar += '<a href="' + self._url + '_' + str(i) + '.html">' + str(i) + '</a>'


# 分页总数控制在100页
def control_page_num(total_page_num, single_page_num):
    if int(total_page_num) / single_page_num > 100:
        total_page_num = 100 * single_page_num
    return total_page_num
