from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admins/$', TemplateView.as_view(template_name="admins.html")),
    url(r'^admins/login/$', views.admin_login, name="Admin Login"),
    url(r'^admins/panel/$', views.admins_panel, name="Admin Panel"),
    url(r'^admins/panel/student/$', views.admins_student_management_section, name="Student Management"),
    url(r'^admins/panel/student/add/$', views.admins_add_student, name="Add Student"),
    url(r'^admins/panel/student/delete/$', views.admins_delete_student, name="Delete Student"),
    url(r'^admins/panel/student/edit/$', views.admins_edit_student, name="Edit Student"),
    url(r'^admins/panel/student/upload/$', views.admins_upload_student, name="Upload Student"),
    url(r'^admins/panel/docs/new/$', views.admins_view_new_docs, name="New Docs"),
    url(r'^student/login/$', views.student_login, name="Student Login"),
    url(r'^logout/$', views.logout_all, name="Logout"),
    url(r'^$', views.index, name="Index"),
]
