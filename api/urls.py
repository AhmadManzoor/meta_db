from django.conf import settings
from django.conf.urls import url
from .views.style import StyleListView
from .views.style import StyleUpdateView
from .views.style import MoreLikeStyleListView
from .views.style import InactivateBrandView
from .views.debug import DebugSearchView
from .views.health import HealthCheckView

urlpatterns = [
    url(r'^update/(?P<site>(os|cm))/styles/$', StyleUpdateView.as_view()),
    url(r'^(?P<site>(os|cm))/styles/$', StyleListView.as_view()),
    url(r'^(?P<site>(os|cm))/styles/(?P<sid>\d+)/more-like/$',
        MoreLikeStyleListView.as_view()),
    url(r'^update/styles/$', StyleUpdateView.as_view()),
    url(r'^styles/$', StyleListView.as_view()),
    url(r'^styles/(?P<sid>\d+)/more-like/$', MoreLikeStyleListView.as_view()),
    url(r'^inactivate-brand/(?P<brand_id>\w+)/$',
        InactivateBrandView.as_view()),
    url(r'^health-check/$', HealthCheckView.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^debug-search/$', DebugSearchView.as_view()),
    ]
