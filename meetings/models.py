from django.db import models
from core.models import User
from meetings.middleware import get_request


class ScheduleMeeting(models.Model):
    METTTING_TIME_INTERVAL = (('15 MIN','15 MIN'), ('30 MIN', '30 MIN'), ('45 MIN','45 MIN'))

    meeting_creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    from_meeting_date_time = models.DateTimeField()
    to_meeting_date_time = models.DateTimeField()
    meeting_time_interval = models.CharField(max_length=30, choices=METTTING_TIME_INTERVAL)
    is_booked = models.BooleanField(default=False)
    user_name = models.CharField(max_length=255, null=True, blank=True)
    user_email = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.meeting_creator.username} {'available' if not self.is_booked else 'unavailable'}"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.meeting_creator = get_request().user
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)