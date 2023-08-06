from django.conf.urls import url
from .views import CreateGroup, AddUser, GroupPermission

urlpatterns = [
    url(r'^permissions/creategroup', CreateGroup.as_view()),
    url(r'^permissions/adduser', AddUser.as_view()),
    url(r'^permissions/grouppermission', GroupPermission.as_view()),
]
