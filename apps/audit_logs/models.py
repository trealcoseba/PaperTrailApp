from django.db import models
from django.contrib.auth.models import User

class AuditLog(models.Model):
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action_type = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=45, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit_logs'

    def __str__(self):
        return f"[{self.timestamp}] {self.action_type} by {self.actor.username if self.actor else 'System'}"