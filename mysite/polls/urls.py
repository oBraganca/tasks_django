from django.urls import include, path

from . import views

urlpatterns = [ 
    path('helloworld/', views.helloWorld),
    path('', views.index, name='home-page'),
    path('task/<int:id>', views.taskView, name='task-view'),
    path('edit/<int:id>', views.editTask, name='edit-task'),
    path('changestatus/<int:id>', views.changeStatus, name='change-status'),
    path('delete/<int:id>', views.deleteTask, name='delete-task'),
    path('newtask/', views.newTask, name='new-task'),
]