from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_proctor = models.BooleanField(default=False)


class Exam(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    duration = models.IntegerField(help_text='Duration in minutes')
    start_time = models.DateTimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)


class Question(models.Model):
    exam = models.ForeignKey(Exam, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    qtype = models.CharField(max_length=10, choices=(('mcq','MCQ'),('sub','Subjective')))
    options = models.JSONField(null=True, blank=True)
    answer = models.JSONField(null=True, blank=True)


class Attempt(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True)


class Response(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.JSONField()
    is_correct = models.BooleanField(null=True)


class ProctorEvent(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=100) # e.g., 'multiple_faces', 'no_face', 'left_room'
    confidence = models.FloatField(null=True)
    metadata = models.JSONField(null=True, blank=True)