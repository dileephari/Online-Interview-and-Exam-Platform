from django.urls import path
from . import views
from .views import logout_view



urlpatterns = [
    path('', views.index, name='home'),
    path('login', views.login_user, name='login'),
    path('register/', views.register,name='register'),
    path('logout/', logout_view, name='logout'),

    path('create_exam/', views.create_exam, name='create_exam'),
    path('exam/<int:exam_id>/take/', views.take_exam, name='take_exam'),
    path('exam/<int:exam_id>/result/', views.exam_result, name='exam_result'),
    path('exam_list/', views.exam_list, name='exam_list'),  # <-- home page
    
 
    
]
