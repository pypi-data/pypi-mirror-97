from django.conf.urls import url

from sbc_drf_authtoken import views

urlpatterns = [
    url(r'login$', views.obtain_auth_token),
    url(r'masquerade$', views.masquerade_login)
]
