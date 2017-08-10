from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^student/login/$', views.student_login, name="Student Login"),
    url(r'^admins/$', TemplateView.as_view(template_name="admins.html")),
    url(r'^admins/login/$', views.admin_login, name="Admin Login"),
    url(r'^admins/panel/$', views.admins_panel, name="Admin Panel"),
    url(r'^admins/panel/student/$', TemplateView.as_view(template_name="st-mg.html"), name="Student Management"),
    url(r'^logout/$', views.logout_all, name="Logout"),
    url(r'^$', views.index, name="Index"),
]
