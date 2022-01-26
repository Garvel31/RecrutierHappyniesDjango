from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import generics

from mixins.soft_delete import DeletableMixin
from rechappines.models import Projects
from rechappines.serializer import ProjectsReadSerializer, ProjectsWriteSerializer, ProjectsArchiveSerializer


class ProjectsArchiveViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects_with_deleted.exclude(deleted_at=None)

    def get_serializer_class(self):
        if self.action in ("partial_update"):
            return ProjectsArchiveSerializer
        return ProjectsReadSerializer


class ProjectsViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        if self.action in ("list", "retrieve"):
            return Projects.objects.all()
        return Projects.objects_with_deleted.all()


    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return ProjectsReadSerializer
        return ProjectsWriteSerializer





