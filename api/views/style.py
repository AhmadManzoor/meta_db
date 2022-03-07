from datetime import datetime, timedelta
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from api.serializers.style import StyleListSerializer
from apps.models.style import StyleListModel, ProductModel
from apps.models.category import StyleCategoryMasterModel, StyleCategorySubModel

# from meta_db.models import ProductModel
from elasticsearch_dsl import Q
from search.handler import SearchHandler


class StyleListView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, site="os", version="v1", format="json"):
        _status = status.HTTP_200_OK
        _data = {
            "message": None,
            "data": None,
        }
        _st_time = datetime.now()
        _query, _page_number, _page_size = self.pre_process_search_request
        if not _query:
            _data["message"] = "please call with search query"
            _status = status.HTTP_400_BAD_REQUEST
        else:
            SearchHandler(site=site).save_query(_query)
            _q = None
            if (
                not _q
                and getattr(StyleListModel.objects, site).filter(id=_query).exists()
            ):
                _q = getattr(StyleListModel.objects, site).filter(id=_query)
            # TODO: comment out because of performance issue in production DB
            # if not _q and StyleListModel.objects.filter(style_number__iexact=_query).exists():
            #     _q = StyleListModel.objects.filter(style_number__iexact=_query)
            if (
                not _q
                and getattr(StyleListModel.objects, site)
                .filter(brand__name__iexact=_query)
                .exists()
            ):
                _q = getattr(StyleListModel.objects, site).filter(
                    brand__name__iexact=_query
                )
                # TODO: price range for style list model
            if _q:
                _start = (_page_number - 1) * _page_size
                _end = _start + _page_size
                _data["data"] = {
                    "total": _q.count(),
                    "docs": StyleListSerializer(_q[_start:_end], many=True).data,
                }
            else:
                # fields
                _fields = [
                    "style_number",
                    "brand_name",
                    "category",
                    "sub_category",
                    "colors",
                    "style_name",
                    "badges",
                ]
                queries = [
                    Q("multi_match", query=_query, fields=_fields),
                ]
                # price filter
                if "hp" in request.GET or "lp" in request.GET:
                    _price_range = {}
                    if "hp" in request.GET and int(request.GET["hp"] or 0) > 0:
                        _price_range["lt"] = int(request.GET["hp"])
                    if "lp" in request.GET and int(request.GET["lp"] or 0) >= 0:
                        _price_range["gt"] = int(request.GET["lp"])
                    if _price_range:
                        queries.append(Q("range", price=_price_range))
                # category filter
                for k, v in (
                    ("sc", "sub_category"),
                    ("mc", "category"),
                    ("gc", "segment"),
                ):
                    if request.GET.get(k):
                        _cq = [
                            request.GET.get(k),
                        ]
                        if k == "sc":
                            _cq = [
                                i.lower()
                                for i in StyleCategorySubModel.objects.values_list(
                                    "name", flat=True
                                ).filter(slug_name=_cq[0])
                            ]
                        elif k == "mc":
                            _cq = [
                                i.lower()
                                for i in StyleCategoryMasterModel.objects.values_list(
                                    "name", flat=True
                                ).filter(slug_name=_cq[0])
                            ]
                        queries.append(Q("terms", **{v: _cq}))
                        break
                _data["data"] = SearchHandler(
                    site=site, page_number=_page_number, page_size=_page_size
                ).search(queries)
        _data["run_time"] = datetime.now() - _st_time
        return Response(data=_data, status=_status)

    @property
    def pre_process_search_request(self):
        _query = (self.request.GET.get("q") or "").strip().replace("+", " ")
        _page_size = 48
        _page_number = 1
        try:
            _page_size = int(self.request.GET.get("page_size") or 48)
            _page_number = int(self.request.GET.get("page_number") or 1)
        except ValueError as e:
            print(e)
            pass
        return _query, _page_number, _page_size


class StyleUpdateView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, site="os", version="v1", format="json"):
        """
        to prevent deleting Styles with future time updated date,
        end time is confined until current time
        """
        _time_from = request.query_params.get("time_from")
        _time_to = request.query_params.get("time_to")

        time_to = None
        if _time_to:
            try:
                time_to = datetime.strptime(_time_to, "%Y%m%d%H%M%S")
            except:
                pass
        if time_to is None:
            time_to = datetime.now()

        time_from = None
        if _time_from:
            try:
                time_from = datetime.strptime(_time_from, "%Y%m%d%H%M%S")
            except:
                pass
        if time_from is None:
            time_from = time_to - timedelta(hours=1)

        _delete = (
            ProductModel.objects.filter(brand__site=site.upper())
            .values_list("id", flat=True)
            .filter(updated__gte=time_from, updated__lte=time_to, _is_active="N")
        )
        _styles = getattr(StyleListModel.objects, site).filter(
            updated_date__gte=time_from, updated_date__lte=time_to
        )
        _hdr = SearchHandler(site=site)

        for d in _delete:
            s = _hdr.get(id=d)
            if s:
                print("[DELETE]", d)
                s.delete()

        for s in _styles:
            print("[CREATE/UPDATED]", s.pk)
            _hdr.create_or_update(s)

        return Response(
            status=status.HTTP_200_OK,
            data={
                "delete": len(_delete),
                "update": _styles.count(),
            },
        )


class InactivateBrandView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, site="os", version="v1", format="json", brand_id=None):
        if brand_id is not None:
            print("[DELETE] brand_id: %s" % brand_id)
            SearchHandler(site=site).delete_inactive_brand(brand_id)
            return Response(status=status.HTTP_200_OK)

        print("[DELETE] brand_id: is None!")
        return Response(status=status.HTTP_400_BAD_REQUEST)


class MoreLikeStyleListView(APIView):

    permission_classes = (AllowAny,)

    def get(self, request, sid, site="os", version="v1", format="json"):
        try:
            _size = 8
            if "size" in request.GET:
                _size = int(request.GET["size"])
            obj = ProductModel.objects.get(pk=sid)
            _params = [
                obj.brand.name,
                obj.os_category_master.display_group,
                obj.os_category_master.name,
            ]
            if getattr(obj, "os_category_sub_id"):
                _params.append(obj.os_category_sub.name)
            _params += [c.color.name for c in obj.colors]
            _data = SearchHandler(site=site).more_like_style(
                sid, " ".join(_params).lower(), _size
            )
            return Response(data=_data)
        except (ProductModel.DoesNotExist, ValueError):
            pass
        return Response(status=status.HTTP_200_OK)
