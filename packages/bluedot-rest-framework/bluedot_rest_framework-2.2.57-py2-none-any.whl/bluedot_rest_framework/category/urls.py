from rest_framework.routers import DefaultRouter

from .views import CategoryView

router = DefaultRouter(trailing_slash=False)

router.register(r'category', CategoryView,
                basename='category')

urlpatterns = router.urls
