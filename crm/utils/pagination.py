from django.utils.safestring import mark_safe

class Pagination:

    def __init__(self, page_num, params,all_count, per_num=10, max_show=11):

        try:
            self.page_num = int(page_num)
            if self.page_num <= 0:
                self.page_num = 1
        except Exception as e:
            self.page_num = 1
        # 总的数据量
        self.all_count = all_count
        # 每页显示的数据条数
        self.per_num = per_num
        # 总页码数
        self.total_page_num, more = divmod(all_count, per_num)
        if more:
            self.total_page_num += 1

        # 最多显示的页面数
        self.max_show = max_show
        self.half_show = max_show // 2
        self.params = params

    @property
    def start(self):
        """
        数据切片的起始值
        :return:
        """
        return (self.page_num - 1) * self.per_num

    @property
    def end(self):
        """
        数据切片的终止值
        :return:
        """
        return self.page_num * self.per_num

    @property
    def page_html(self):
        if self.total_page_num < self.max_show:
            page_start = 1
            page_end = self.total_page_num
        elif self.page_num <= self.half_show:
            page_start = 1
            page_end = self.max_show
        elif self.page_num + self.half_show > self.total_page_num:
            page_start = self.total_page_num - self.max_show + 1
            page_end = self.total_page_num

        else:
            # 起始的页面
            page_start = self.page_num - self.half_show
            # 终止的页码
            page_end = self.page_num + self.half_show

        page_list = []

        # 上一页
        if self.page_num == 1:
            page_list.append('<li class="disabled" ><a >上一页</a></li>')
        else:
            self.params['page'] = self.page_num - 1
            page_list.append('<li ><a href="?{}">上一页</a></li>'.format(self.params.urlencode()))

        for i in range(page_start, page_end + 1):
            self.params['page'] = i
            if i == self.page_num:
                page_list.append('<li class="active" ><a href="?{}">{}</a></li>'.format(self.params.urlencode(), i))
            else:
                page_list.append('<li><a href="?{}">{}</a></li>'.format(self.params.urlencode(), i))

        if self.page_num == self.total_page_num:
            page_list.append('<li class="disabled"><a>下一页</a></li>')
        else:
            self.params['page'] = self.page_num + 1
            page_list.append('<li><a href="?{}">下一页</a></li>'.format(self.params.urlencode()))

        return mark_safe(''.join(page_list))
