from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('personnel', 'Office Personnel'),
        ('admin', 'Administrator'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='student')
    office = models.ForeignKey('offices.Office', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff_members')

    class Meta:
        db_table = 'profile_profile'

    def __str__(self):
        return f"{self.user.username} ({self.role})"