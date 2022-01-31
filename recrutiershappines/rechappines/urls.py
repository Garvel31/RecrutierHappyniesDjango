from django.contrib import admin
from django.urls import path, include, re_path

from rechappines import views

urlpatterns = [
    path('file/', views.FileTestViewSet.as_view({'post': 'create'}), name='file'),
    path('technology/', views.TechnologyViewSet.as_view({'get': 'list'}), name='technology'),
    path('projects/info/', views.ProjectsShortInfoViewSet.as_view({'get': 'list'}), name='projects-info'),
    path('projects/archive/', views.ProjectsArchiveViewSet.as_view({'get': 'list'}), name='projects-archive'),
    path('projects/archive/<pk>/', views.ProjectsArchiveViewSet.as_view({'get': 'retrieve',
                                                                        'post': 'restore_project'}),
                                                                        name='projects-archive'),
    path('projects/', views.ProjectsViewSet.as_view({'get': 'list', 'post': 'create'}), name='projects'),
    path('projects/<pk>/', views.ProjectsViewSet.as_view({'get': 'retrieve',
                                                        'patch': 'partial_update',
                                                        'delete': 'destroy',
                                                        'put': 'update'}), name='projects'),

]
