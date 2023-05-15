from django.contrib import admin
from django.urls import path,include
from App import views
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('logins/',views.logins,name="logins"),
    path('logouts/',views.logouts,name="logouts"),
    path('password_change/',views.password_change,name="password_change"),
    path('upload_data/',views.upload_data,name="upload_data"),
    path('upload_questions/',views.upload_questions,name="upload_questions"),
    path('branch/',views.branch,name="branch"),
    path('branch_update/<str:br_id>',views.branch_update,name="branch_update"),
    path('exam_update/<str:ex_id>',views.exam_update,name="exam_update"),
    path('semester/',views.semester,name="semester"),
    path('semester_update/<str:sem_id>',views.semester_update,name="semester_update"),
    path('subject/',views.subject,name="subject"),
    path('subject_update/<str:su_id>',views.subject_update,name="subject_update"),
    path('proctor/',views.proctor,name="proctor"),
    path('proctor_view/<str:pr_id>',views.proctor_view,name="proctor_view"),
    path('exam/',views.exam,name="exam"),
    path('exam_add/',views.exam_add,name="exam_add"),
    path('exam_view/<str:ex_id>',views.exam_view,name="exam_view"),
    path('students/',views.students,name="students"),
    path('student_add/',views.student_add,name="student_add"),
    path('student_view/<str:st_id>',views.student_view,name="student_view"),
    path('question_add/<str:ex_id>',views.question_add,name="question_add"),
    path('question_view/<str:qs_id>',views.question_view,name="question_view"),
    path('update_college/<str:c_id>',views.update_college,name="update_college"),
    path('subject_delete/<str:dl_id>',views.subject_delete,name="subject_delete"),
    path('semester_delete/<str:dl_id>',views.semester_delete,name="semester_delete"),
    path('branch_delete/<str:dl_id>',views.branch_delete,name="branch_delete"),
    path('student_delete/<str:dl_id>',views.student_delete,name="student_delete"),
    path('question_delete/<str:dl_id>',views.question_delete,name="question_delete"),
    path('exam_delete/<str:dl_id>',views.exam_delete,name="exam_delete"),
    path('proctor_delete/<str:dl_id>',views.proctor_delete,name="proctor_delete"),
    url(r'^media/(?P<path>.*)$', serve,{'document_root':  settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path('tinymce/', include('tinymce.urls')),
    path('ajax/load-subject/', views.load_subject, name='ajax_load_subject'), # AJAX
    path('exam_done/',views.exam_done,name="exam_done"),
    path('exam_attend_students/<str:ex_id>',views.exam_attend_students,name="exam_attend_students"),
    path('student_answer_demo/<str:std_id>/<str:ex_id>',views.student_answer_demo,name="student_answer_demo"),
    path('viewPdf/<str:std_id>/<str:ex_id>',views.viewPdf,name="viewPdf"),
    path('downloadPdf/<str:std_id>/<str:ex_id>',views.downloadPdf,name="downloadPdf"),
    path('send_test_result/<str:ex_id>',views.send_test_result,name="send_test_result"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
