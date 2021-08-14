from django.urls import path
from .views import *


app_name = "main"
urlpatterns = [
    # ----------------------------------------------
    # task urls
    # ----------------------------------------------
    path("task-create", TaskCreate.as_view(), name="task-create"),

    # ----------------------------------------------
    # task urls
    # ----------------------------------------------


    path('', LandingView.as_view(), name="landing_page"),
    path('all-tasks', AllTaskes.as_view(), name="all-tasks"),
    path('tasks-apis', AllTaskAPI.as_view(), name='tasks-apis'),
    path('tasks/<int:pk>/rud', TaskDetails.as_view(), name='tasks-rud'),
    path('users/', UserList.as_view(), name='users-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name= 'user-detail'),

    path('task_in_page/<int:pk>/update', update_task_in_page, name="update_in_html"),
    path('task_in_page/<int:pk>/<int:user_pk>/assign', assigne_task, name="assign_in_html"),
    path('task_in_page/<int:pk>/start', start_task, name="start_in_html"),
    path('task_in_page/<int:pk>/stop', stop_task, name="stop_in_html"),
    path('task_in_page/<int:pk>/upload_to_reveiw', upload_to_test_task, name="to_review_in_html"),
    path('task_in_page/<int:pk>/resume', resume_task, name="resume_in_html"),
    path('task_in_page/<int:pk>/validate', validate_task, name="validate_in_html"),
    path('task_in_page/<int:pk>/to_reveiw', mark_as_to_reveiw_task, name="to_reveiw_in_html"),
    path('task_in_page/<int:pk>/start_reveiw', start_reveiw_task, name="start_reveiw_in_html"),

    path("test-form",get_name_from_form, name="test-form")
]
