class RangePaginationMixin(object):
    """
        Добавляет в контекс переменную pag_range,
        которая позволяет выводить в списке страниц 
        только заданный диапозон, а не все страницы
    """
    left_page_range = 3
    right_page_range = 2

    def get_pag_range(self, current_page, page_range):
        if current_page - self.left_page_range < 1:
            left_range = 0
        else:
            left_range = current_page - self.left_page_range
        rigth_range = current_page + self.right_page_range
        return page_range[left_range:rigth_range]

    def get_context_data(self, *args, **kwargs):
        context = super(RangePaginationMixin, self).get_context_data(*args, **kwargs)
        current_page = context['page_obj'].number
        context['pag_range'] = self.get_pag_range(current_page, context['paginator'].page_range)
        return context


class CurrentGetParamsMixin(object):
    """
        Добавляет в контекст строку содержащую
        GET параметры для данного запроса
        чтобы подставить их в пагинацию
    """

    def get_current_get_params(self):
        if not self.request.GET:
            return ''
        params = ''
        for key in list(self.request.GET.keys()):
            if key == 'page':
                continue
            params = '{}&{}={}'.format(params, key, self.request.GET.get(key))
        return params
    
    def get_context_data(self, **kwargs):
        context = super(CurrentGetParamsMixin, self).get_context_data(**kwargs)
        context['current_get_params'] = self.get_current_get_params()
        return context