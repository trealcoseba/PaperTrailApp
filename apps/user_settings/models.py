from django.db import models
from django.contrib.auth.models import User

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    dark_mode = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)

    class Meta:
        db_table = 'user_settings_usersettings'

    def __str__(self):
        return f"Settings for {self.user.username}"