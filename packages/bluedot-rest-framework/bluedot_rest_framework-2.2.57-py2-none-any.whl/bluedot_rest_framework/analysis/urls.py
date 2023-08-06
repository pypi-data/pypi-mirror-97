from rest_framework.routers import DefaultRouter
from .monitor.views import AnalysisMonitorView

router = DefaultRouter(trailing_slash=False)

router.register(r'analysis/monitor', AnalysisMonitorView,
                basename='analysis-monitor')

urlpatterns = router.urls
