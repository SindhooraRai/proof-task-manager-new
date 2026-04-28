from django.urls import path
from .views import task_list, submission_list,update_task

urlpatterns = [
    path('tasks/', task_list),
    path('submissions/', submission_list),
    path('tasks/<int:pk>/update/', update_task),
]