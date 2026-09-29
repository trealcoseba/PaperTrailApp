from django.db import models
from django.contrib.auth.models import User

class DocumentRequest(models.Model):
    STATUS_CHOICES = [
        ('Submitted', 'Submitted'),
        ('Under Review', 'Under Review'),
        ('For Signature', 'For Signature'),
        ('Approved', 'Approved'),
        ('Returned', 'Returned for Revision'),
        ('Released', 'Released'),
    ]

    tracking_number = models.CharField(max_length=32, unique=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_requests')
    template = models.ForeignKey('workflows.WorkflowTemplate', on_delete=models.PROTECT, related_name='requests')
    document_title = models.CharField(max_length=200)
    purpose = models.TextField()
    current_step_order = models.IntegerField(default=1)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Submitted')
    qr_code_url = models.CharField(max_length=255, blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'document_requests'

    def __str__(self):
        return f"{self.tracking_number} - {self.document_title}"


class DocumentStageLog(models.Model):
    document = models.ForeignKey(DocumentRequest, on_delete=models.CASCADE, related_name='stage_logs')
    step_order = models.IntegerField()
    office = models.ForeignKey('offices.Office', on_delete=models.PROTECT, related_name='stage_logs')
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_stages')
    action_taken = models.CharField(max_length=50)
    remarks = models.TextField(blank=True, null=True)
    entered_at = models.DateTimeField(auto_now_add=True)
    action_at = models.DateTimeField(null=True, blank=True)
    duration_hours = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'document_stage_logs'
        ordering = ['step_order']

    def __str__(self):
        return f"{self.document.tracking_number} (Step {self.step_order}) - {self.action_taken}"