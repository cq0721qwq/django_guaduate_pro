'''自定义的分页组件'''
# 如想使用，则需要做以下几件事：、def phone_list(request):
# 根据自身的使用情况来筛选自己的数据
#     queryset = models.PhoneNumInfo.objects.filter(**data_dict).order_by("-level")

# 实例化类
#     page_obj = Pagination(request, queryset)

# 获得分完页的数据
#     page_queryset = page_obj.page_query

# 获得页码
#     page_str = page_obj.html()

# 渲染html文件即可，给html传递page_queryset以及page_str
#     return render(request, 'phone_list.html', {'queryset': page_queryset, 'page_str': page_str})

from django.utils.safestring import mark_safe


class Pagination(object):
    def __init__(self, request, queryset, page_size=10, plus=5, page_param="page"):
        '''
        :param request: 请求的对象
        :param queryset: 符合条件的数据
        :param page_size: 页面的大小，默认是10
        :param plus:显示当前页的前后若干页
        :param page_param:在URL中传递获取分页的参数
        '''
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        page = request.GET.get(page_param, "1")
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        self.page_param = page_param
        self.page = page
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size

        self.page_query = queryset[self.start:self.end]
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, page_size)
        if (div):
            total_page_count += 1
        self.total_page_count = total_page_count
        self.plus = plus

    def html(self):
        start_page = max(self.page - self.plus, 1)
        # max_page = int(self.total_page_count / self.page_size) + 1
        end_page = min(self.page + self.plus, self.total_page_count + 1)

        page_str_list = []
        # self.query_dict.setlist(self.page_param,[1])
        # page_str_list.append('<li class = "active"><a href="?page={}">{}</a></li>')
        for i in range(start_page, end_page):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class = "active"><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)
        page_str = mark_safe("".join(page_str_list))
        return page_str
