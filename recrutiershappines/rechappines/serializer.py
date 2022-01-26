from rest_framework import serializers

from rechappines.models import Projects, TeamsInfo, ProjectsType, WorkingCondition


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


class ProjectsWriteSerializer(serializers.ModelSerializer):
    project_type = ProjectsTypeSerializer()
    team_info = TeamsInfoSerializer()
    working_conditions = WorkingConditionSerializer()

    class Meta:
        model = Projects
        fields = ("id", "created", "updated", "project_name", "customer", "proj_stage",
                  "technology", "func_direction", "subject_area", "active",
                  "draft", "project_type", "team_info", "working_conditions", "project_type_id", "team_info_id",
                  "working_conditions_id")

    def create(self, validated_data):
        project_type_data = validated_data.pop('project_type')
        team_info_data = validated_data.pop('team_info')
        working_conditions_data = validated_data.pop('working_conditions')
        pt = ProjectsType.objects.create(**project_type_data)
        ti = TeamsInfo.objects.create(**team_info_data)
        wc = WorkingCondition.objects.create(**working_conditions_data)
        project = Projects.objects.create(project_type=pt, team_info=ti, working_conditions=wc, **validated_data)

        return project

    def update(self, instance, validated_data):
        project_type_data = validated_data.pop('project_type')
        team_info_data = validated_data.pop('team_info')
        working_conditions_data = validated_data.pop('working_conditions')

        project_type = instance.project_type
        team_info = instance.team_info
        working_conditions = instance.working_conditions

        instance.created = validated_data.get('created', instance.created)
        instance.updated = validated_data.get('updated', instance.updated)
        instance.project_name = validated_data.get('project_name', instance.project_name)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.proj_stage = validated_data.get('proj_stage', instance.proj_stage)
        instance.technology = validated_data.get('technology', instance.technology)
        instance.func_direction = validated_data.get('func_direction', instance.func_direction)
        instance.subject_area = validated_data.get('subject_area', instance.subject_area)
        instance.active = validated_data.get('active', instance.active)
        instance.draft = validated_data.get('draft', instance.draft)
        instance.save()

        project_type.isPayType = project_type_data.get('isPayType', project_type.isPayType)
        project_type.isPO = project_type_data.get('isPO', project_type.isPO)
        project_type.isMVP = project_type_data.get('isMVP', project_type.isMVP)
        project_type.isFromScratch = project_type_data.get('isFromScratch', project_type.isFromScratch)
        project_type.save()

        team_info.devMetodology = team_info_data.get('devMetodology', team_info.devMetodology)
        team_info.analitics = team_info_data.get('analitics', team_info.analitics)
        team_info.tester = team_info_data.get('tester', team_info.tester)
        team_info.back = team_info_data.get('back', team_info.back)
        team_info.front = team_info_data.get('front', team_info.front)
        team_info.save()

        working_conditions.adress = working_conditions_data.get('adress', working_conditions.adress)
        working_conditions.procedure = working_conditions_data.get('procedure', working_conditions.procedure)
        working_conditions.isOvertimeExpect = working_conditions_data.get('isOvertimeExpect', working_conditions.isOvertimeExpect)
        working_conditions.save()

        return instance
