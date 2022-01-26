from django.contrib import admin
from django.urls import path, include, re_path

from rechappines import views

urlpatterns = [
    path('projects/', views.ProjectsViewSet.as_view({'get': 'list', 'post': 'create'}), name='projects'),
    path('projects/<pk>/', views.ProjectsViewSet.as_view({'get': 'retrieve',
                                                        'patch': 'partial_update',
                                                        'delete': 'destroy',
                                                          'put': 'update'}), name='projects'),
]
