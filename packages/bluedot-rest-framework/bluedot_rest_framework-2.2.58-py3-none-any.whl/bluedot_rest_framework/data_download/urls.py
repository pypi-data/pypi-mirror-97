from rest_framework.routers import DefaultRouter
from bluedot_rest_framework import import_string

DataDownloadView = import_string('data_download.views')
DataDownloadUserView = import_string('data_download.user_views')

router = DefaultRouter(trailing_slash=False)

router.register(r'data-download/user', DataDownloadUserView,
                basename='data-download-user')
router.register(r'data-download', DataDownloadView,
                basename='data-download')

urlpatterns = router.urls
