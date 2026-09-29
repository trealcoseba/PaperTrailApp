from django.db import models

class WorkflowTemplate(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    estimated_total_days = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'workflow_templates'

    def __str__(self):
        return self.title


class WorkflowTemplateStep(models.Model):
    template = models.ForeignKey(WorkflowTemplate, on_delete=models.CASCADE, related_name='steps')
    step_order = models.IntegerField()
    office = models.ForeignKey('offices.Office', on_delete=models.CASCADE, related_name='template_steps')
    required_action = models.CharField(max_length=50)
    expected_duration_days = models.IntegerField(default=1)

    class Meta:
        db_table = 'workflow_template_steps'
        ordering = ['step_order']

    def __str__(self):
        return f"{self.template.title} - Step {self.step_order}: {self.office.code}"