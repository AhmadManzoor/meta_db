from django.db.models.query import QuerySet


class Paginator(object):
    def __init__(self, request, data, scope=20):
        self.request = request
        self.data = data
        self.scope = scope
        self.page = None
        self.current = 1
        self.next = None
        self.previous = None
        self.pages = 1
        self.number_of_items = 0

    def _is_query_set(self):
        return isinstance(self.data, QuerySet)

    def _max_page(self):
        _page_num = 1
        if 'page' in self.request.GET.keys():
            try:
                _page_num = int(self.request.GET['page'])
            except ValueError as e:
                print("[Pagination]", e)
                pass
        # max page
        if _page_num > self.number_of_items // self.scope + 1:
            _page_num = self.number_of_items // self.scope + 1
        # min page
        if _page_num <= 1:
            _page_num = 1
        self.current = _page_num

    def _has_next(self):
        if self.current < self.pages:
            self.next = self.current + 1

    def _has_previous(self):
        if self.current >= 2:
            self.previous = self.current - 1

    def _get_pages(self):
        self.pages = (self.number_of_items - 1) // self.scope + 1

    def _get_page(self):
        _min = (self.current - 1) * self.scope
        _max = min(_min + self.scope, self.number_of_items)
        self.page = self.data[_min: _max]

    @property
    def dispatch(self):
        pagination = {
            'current': self.current,
            'next': self.next,
            'previous': self.previous,
            'pages': self.pages,
            'total': self.number_of_items,
            'page_size': self.scope,
        }
        return self.page, pagination

    @property
    def paginate(self):
        if self._is_query_set():
            self.number_of_items = self.data.count()
        else:
            self.number_of_items = len(self.data)

        # base condition
        if self._is_query_set():
            if not self.data.exists():
                return self.dispatch
        else:
            if not self.data:
                return self.dispatch

        self._max_page()
        self._get_pages()
        self._get_page()
        self._has_next()
        self._has_previous()

        return self.dispatch
