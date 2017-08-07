from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'student/login/', views.student_login, name="Student Login"),
    url(r'^logout/$', views.logout, name="Logout"),
    url(r'^$', views.index, name="Index"),
]
