import pathlib
import re

from django.db import transaction
from django.db.models.fields.files import FieldFile
from rest_framework import serializers

from rechappines.models import Projects, TeamsInfo, ProjectsType, WorkingCondition, Technology, FileTest


class FileTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileTest
        fields = ['file', 'file_custom_name']

    @transaction.atomic()
    def create(self, validated_data):
        file = validated_data.pop('file')
        file_custom_name = validated_data.pop('file_custom_name')


        # file_path = file.name  # сохраняем путь к месту откуда загружен файл
        path_obj = pathlib.Path(file.name)
        # print('file_custom_name= ', file_custom_name)
        # print("path_obj =", path_obj)
        suffix = path_obj.suffix
        # if file_custom_name != None:
        #     file.name = file_custom_name + suffix  # если было введено custom_file_name генерируем новое имя файла
        #     path_obj = pathlib.Path(file.name)

        return FileTest.objects.create(
            file=file,
            file_path=file.name,
            file_name=path_obj.stem,
            file_custom_name=file_custom_name,
            file_ext=suffix,  # path_obj.suffix,
        )


class ProjectsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectsType
        fields = ("id", "isPayType",
                  "isPO",
                  "isMVP",
                  "isFromScratch")


class TeamsInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamsInfo
        fields = ("id", "devMetodology",
                  "analitics",
                  "tester",
                  "back",
                  "front")


class WorkingConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingCondition
        fields = ("id", "adress",
                  "procedure",
                  "isOvertimeExpect")


class ProjectsReadSerializer(serializers.ModelSerializer):
    project_type = ProjectsTypeSerializer()
    team_info = TeamsInfoSerializer()
    working_conditions = WorkingConditionSerializer()

    class Meta:
        model = Projects
        exclude = []


class TechnologySerializer(serializers.ModelSerializer):

    class Meta:
        model = Technology
        fields = ['tech']


class ProjectsShortInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ['id',
                  'created',
                  'project_name',
                  'customer',
                  'proj_stage']



class ProjectsWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ("id", "created", "updated", "project_name", "customer", "proj_stage",
                  "technology", "func_direction", "subject_area",
                  "draft", "deleted_at", "project_type", "team_info", "working_conditions", "project_type_id",
                  "team_info_id",
                  "working_conditions_id")

    project_type = ProjectsTypeSerializer()
    team_info = TeamsInfoSerializer()
    working_conditions = WorkingConditionSerializer()

    def create(self, validated_data):
        project_type_data = validated_data.pop('project_type')
        team_info_data = validated_data.pop('team_info')
        working_conditions_data = validated_data.pop('working_conditions')
        pt = ProjectsType.objects.create(**project_type_data)
        ti = TeamsInfo.objects.create(**team_info_data)
        wc = WorkingCondition.objects.create(**working_conditions_data)
        project = Projects.objects.create(project_type=pt, team_info=ti, working_conditions=wc, **validated_data)


        techs_from_request = re.split(", | |; ", project.technology) #сплитим все прописанные при создании этого проекта технологии
        db_techs = Technology.objects.all() #берем все записи из таблицы Technology
        array_db_tech=[]
        for db_tech in db_techs:
            array_db_tech.append(db_tech.tech)  #Берем все значения поля tech
        for tech in techs_from_request:
            if tech not in array_db_tech:
                serializer = TechnologySerializer(data={'tech':f'{tech}'})
                serializer.is_valid()
                serializer.save()
        return project

    @transaction.atomic()
    def update(self, instance, validated_data):

        if 'project_type' in validated_data.keys():
            project_type_data = validated_data.pop('project_type')
            project_type = instance.project_type
            project_type.isPayType = project_type_data.get('isPayType', project_type.isPayType)
            project_type.isPO = project_type_data.get('isPO', project_type.isPO)
            project_type.isMVP = project_type_data.get('isMVP', project_type.isMVP)
            project_type.isFromScratch = project_type_data.get('isFromScratch', project_type.isFromScratch)
            project_type.save()

        if 'team_info' in validated_data.keys():
            team_info_data = validated_data.pop('team_info')
            team_info = instance.team_info
            team_info.devMetodology = team_info_data.get('devMetodology', team_info.devMetodology)
            team_info.analitics = team_info_data.get('analitics', team_info.analitics)
            team_info.tester = team_info_data.get('tester', team_info.tester)
            team_info.back = team_info_data.get('back', team_info.back)
            team_info.front = team_info_data.get('front', team_info.front)
            team_info.save()

        if 'working_conditions' in validated_data.keys():
            working_conditions_data = validated_data.pop('working_conditions')
            working_conditions = instance.working_conditions
            working_conditions.adress = working_conditions_data.get('adress', working_conditions.adress)
            working_conditions.procedure = working_conditions_data.get('procedure', working_conditions.procedure)
            working_conditions.isOvertimeExpect = working_conditions_data.get('isOvertimeExpect',
                                                                              working_conditions.isOvertimeExpect)
            working_conditions.save()

        return super().update(instance, validated_data)




