from django.db import models

from mixins.soft_delete import DeletableMixin


class ProjectsType(models.Model):
    isPayType = models.BooleanField(default=False)
    isPO = models.BooleanField(default=False)
    isMVP = models.BooleanField(default=True)
    isFromScratch = models.BooleanField(default=False)


class TeamsInfo(models.Model):
    devMetodology = models.CharField(max_length=101)
    analitics = models.IntegerField(default=0)
    tester = models.IntegerField(default=0)
    back = models.IntegerField(default=0)
    front = models.IntegerField(default=0)


class Technology(models.Model):
    tech = models.CharField(max_length=100, primary_key=True)


class WorkingCondition(models.Model):
    adress = models.CharField(max_length=101)
    procedure = models.CharField(max_length=100)
    isOvertimeExpect = models.BooleanField(default=False)


class Projects(DeletableMixin, models.Model):
    created = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    updated = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    project_name = models.CharField(max_length=101)
    customer = models.CharField(max_length=100)
    proj_stage = models.CharField(max_length=100)
    technology = models.CharField(max_length=100)
    func_direction = models.CharField(max_length=100)
    subject_area = models.CharField(max_length=100)
    draft = models.BooleanField(default=False)
    project_type = models.ForeignKey(ProjectsType, related_name='projects', on_delete=models.CASCADE)
    team_info = models.ForeignKey(TeamsInfo, related_name='projects', on_delete=models.CASCADE)
    working_conditions = models.ForeignKey(WorkingCondition, related_name='projects', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']


