from django.shortcuts import render
from rest_framework import viewsets

from rechappines.models import Projects
from rechappines.serializer import ProjectsReadSerializer, ProjectsWriteSerializer


class ProjectsViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsWriteSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ProjectsReadSerializer
        return ProjectsWriteSerializer

#TODO soft delete
