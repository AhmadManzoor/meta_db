from django.shortcuts import render
from django.views.generic import View
from search.handler import SearchHandler
from apps.models.style import StyleListModel
from api.serializers.style import StyleListSerializer


class DebugSearchView(View):
    def get(self, request, version='v1'):
        _query = request.GET.get('q').strip()
        _result = {
            'total': 0,
            'docs': [],
        }
        _q = None
        if not _query:
            raise Exception('no query error')
        if not _q and StyleListModel.objects.filter(id=_query).exists():
            _q = StyleListModel.objects.filter(id=_query)
        if not _q and StyleListModel.objects.filter(
                style_number__iexact=_query).exists():
            _q = StyleListModel.objects.filter(style_number__iexact=_query)
        if not _q and StyleListModel.objects.filter(
                brand__name__iexact=_query).exists():
            _q = StyleListModel.objects.filter(brand__name__iexact=_query)
        if _q:
            _result = {
                'total': _q.count(),
                'docs': StyleListSerializer(_q, many=True).data
            }
        else:
            _result = SearchHandler().search(_query)
        return render(request, "debug.html", _result)
