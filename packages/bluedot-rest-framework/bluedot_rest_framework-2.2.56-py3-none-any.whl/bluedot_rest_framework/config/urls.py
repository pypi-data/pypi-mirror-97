from rest_framework.routers import DefaultRouter
from bluedot_rest_framework import import_string

ConfigView = import_string('config.views')
router = DefaultRouter(trailing_slash=False)

router.register(r'config', ConfigView,
                basename='config')

urlpatterns = router.urls
