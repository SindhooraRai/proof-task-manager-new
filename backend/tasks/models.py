from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):#creating a table named task
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('SUBMITTED', 'Submitted'),
        ('REVIEWED', 'Reviewed'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    PRIORITY_CHOICES = [
    ('LOW', 'Low'),
    ('MEDIUM', 'Medium'),
    ('HIGH', 'High'),
    ]
    title = models.CharField(max_length=100)#textfield with limit
    description = models.TextField()#no limit for textfield
    deadline = models.DateTimeField() #store date and time
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='TODO')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    created_by = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    related_name='created_tasks'
)

    assigned_to = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True,
    related_name='assigned_tasks'
)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Submission(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='submissions')
    description = models.TextField()
    link = models.URLField(blank=True, null=True)
    file = models.FileField(upload_to='submissions/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    REVIEW_STATUS = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    review_status = models.CharField(
        max_length=20,
        choices=REVIEW_STATUS,
        default='PENDING'
    )

    feedback = models.TextField(blank=True, null=True)

    reviewed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_submissions'
    )

    def __str__(self):
        return f"{self.user} - {self.task}"