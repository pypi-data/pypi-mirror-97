from rest_framework.routers import DefaultRouter
from bluedot_rest_framework import import_string


UserView = import_string('user.views')

router = DefaultRouter(trailing_slash=False)
router.register(r'user', UserView, basename='user')
urlpatterns = router.urls
