from django.conf.urls import url
from . import views
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^admins/$', TemplateView.as_view(template_name="admins.html")),
    url(r'^admins/login/$', views.admin_login, name="Admin Login"),
    url(r'^admins/panel/$', views.admins_panel, name="Admin Panel"),
    url(r'^admins/panel/setting/$', views.admins_setting, name="Admin Setting"),
    url(r'^admins/panel/setting/add/PrimaryDoc/$', views.add_main_doc, name="Add Main Doc"),
    url(r'^admins/panel/setting/edit/PrimaryDoc/$', views.edit_main_document, name="Edit Main Doc"),
    url(r'^admins/panel/setting/delete/PrimaryDoc/$', views.delete_main_document, name="Delete Main Doc"),
    url(r'^admins/panel/setting/ChangePassword/$', views.admins_password_change, name="Admin Change Password"),
    url(r'^admins/panel/student/$', views.admins_student_management_section, name="Student Management"),
    url(r'^admins/panel/student/add/$', views.admins_add_student, name="Add Student"),
    url(r'^admins/panel/student/delete/$', views.admins_delete_student, name="Delete Student"),
    url(r'^admins/panel/student/edit/$', views.admins_edit_student, name="Edit Student"),
    url(r'^admins/panel/student/upload/$', views.admins_upload_student, name="Upload Student"),
    url(r'^admins/panel/student/view/$', views.admins_view_students, name="View Student"),
    url(r'^admins/panel/student/report/$', views.view_report, name="View Report"),
    url(r'^admins/panel/student/report/get/$', views.get_report, name="Get Report"),
    url(r'^admins/panel/docs/new/$', views.admins_view_new_docs, name="New Docs"),
    url(r'^admins/panel/docs/status/$', views.accept_reject_docs, name="Docs Change Status"),
    url(r'^admins/panel/staff/$', views.admins_staff_management, name="Staff Management"),
    url(r'^admins/panel/staff/add/$', views.add_staffer, name="Add Staff"),
    url(r'^admins/panel/staff/delete/$', views.delete_staffer, name="Delete Staff"),
    url(r'^admins/panel/education/$', views.education_page, name="Education Management"),
    url(r'^admins/panel/education/subject/edit/$', views.edit_subject, name="Edit Subject"),
    url(r'^admins/panel/education/subject/delete/$', views.delete_subject, name="Delete Subject"),
    url(r'^admins/panel/education/subject/add/$', views.add_subject, name="Add Subject"),
    url(r'^admins/panel/education/section/edit/$', views.edit_section, name="Edit Section"),
    url(r'^admins/panel/education/section/delete/$', views.delete_section, name="Delete Section"),
    url(r'^admins/panel/education/section/add/$', views.add_section, name="Add Section"),
    url(r'^student/login/$', views.student_login, name="Student Login"),
    url(r'^student/get/college_number/$', views.get_student_number, name="Student Get College Number"),
    url(r'^upload/$', views.upload_document, name="Upload"),
    url(r'^media/', views.media, name="Media"),
    url(r'^logout/$', views.logout_all, name="Logout"),
    url(r'^$', views.index, name="Index"),
]

