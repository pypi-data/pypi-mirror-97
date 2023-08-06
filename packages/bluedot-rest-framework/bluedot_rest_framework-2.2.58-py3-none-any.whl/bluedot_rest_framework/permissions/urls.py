from django.conf.urls import url
from .views import CreateGroup

urlpatterns = [
    url(r'^permissions/creategroup', CreateGroup),
]
