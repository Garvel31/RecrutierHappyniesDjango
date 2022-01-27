
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rechappines.models import Projects, Technology
from rechappines.serializer import ProjectsReadSerializer, ProjectsWriteSerializer, ProjectsShortInfoSerializer, \
    TechnologySerializer


class ProjectsShortInfoViewSet(viewsets.ModelViewSet):
    queryset = Projects.objects.all()
    serializer_class = ProjectsShortInfoSerializer


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


class TechnologyViewSet(viewsets.ModelViewSet):
    queryset = Technology.objects.all()
    serializer_class = TechnologySerializer





