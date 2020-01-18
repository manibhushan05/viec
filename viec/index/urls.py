from django.urls import re_path

from index.views import UserLogin, UserLogout

index_url_pattern = [
    re_path(r'^login/$', UserLogin.as_view(), name='login'),
    re_path(r'^logout/$', UserLogout.as_view(), name='logout'),
]
