from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.decorators import action

from mixins.soft_delete import DeletableMixin
from rechappines.models import Projects
from rechappines.serializer import ProjectsReadSerializer, ProjectsWriteSerializer


class ProjectsArchiveViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects_with_deleted.exclude(deleted_at=None)
    serializer_class = ProjectsReadSerializer

    @action(detail=False)
    def restore_project(self, request, *args, **kwargs):
        project = Projects.objects_with_deleted.filter(id= self.kwargs.get('pk')).first()
        project.restore()
        data = ProjectsReadSerializer(project).data
        return Response(data=data)



class ProjectsViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        if self.action in ("list", "retrieve"):
            return Projects.objects.all()
        return Projects.objects_with_deleted.all()


    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ProjectsReadSerializer
        return ProjectsWriteSerializer





