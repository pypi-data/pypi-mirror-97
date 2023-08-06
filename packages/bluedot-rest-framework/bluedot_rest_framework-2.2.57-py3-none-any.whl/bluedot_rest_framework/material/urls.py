from rest_framework.routers import DefaultRouter
from bluedot_rest_framework import import_string


MaterialView = import_string('material.views')
TagsView = import_string('material.tags.views')


router = DefaultRouter(trailing_slash=False)
router.register(r'material/tags', TagsView, basename='material-tags')
router.register(r'material', MaterialView, basename='material')


urlpatterns = router.urls
