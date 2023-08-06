from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from .views import AuthGroupViewSet, AuthMenuViewSet, AuthUserViewSet


router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^auth/login', obtain_jwt_token),

]
router.register(r'auth/group', AuthGroupViewSet, basename='auth-group')
router.register(r'auth/menu', AuthMenuViewSet, basename='auth-menu')
router.register(r'auth/user', AuthUserViewSet, basename='auth-user')
urlpatterns += router.urls
