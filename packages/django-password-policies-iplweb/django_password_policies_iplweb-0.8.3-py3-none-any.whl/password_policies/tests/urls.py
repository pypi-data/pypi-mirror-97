from django.conf.urls import include, url

try:
    from django.conf.urls import patterns
except ImportError:
    patterns = False

from password_policies.tests.views import TestHomeView, TestLoggedOutMixinView


urlpatterns = [
    url(r"^password/", include("password_policies.urls")),
    url(r"^$", TestHomeView.as_view(), name="home"),
    url(r"^fubar/", TestLoggedOutMixinView.as_view(), name="loggedoutmixin"),
]

if patterns:
    urlpatterns = patterns("", *urlpatterns)  # noqa
