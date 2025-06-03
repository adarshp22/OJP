from . import views
from django.urls import path
urlpatterns = [
    path('', views.oj_list,name='oj_list'),
    path('create/', views.oj_create,name='oj_create'),
    path('<int:oj_id>/edit/', views.oj_edit,name='oj_edit'),
    path('<int:oj_id>/delete/', views.oj_delete,name='oj_delete'),
    path('register/', views.register,name='register'),
    path('submit/', views.submit,name='submit'),
    path("problem_topics/", views.problem_topics, name="problem_topics"),
    path("topic_problems/<int:id>/", views.topic_problems, name="topic_problems"),
    path('solve/<int:id>/', views.solve_problem, name='solve_problem'),


] 