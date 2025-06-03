from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class OJ(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    text=models.TextField(max_length=240)
    photo=models.ImageField(upload_to='photos/', blank=True, null=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'
    


class CodeSubmission(models.Model):
    language = models.CharField(max_length=100)
    code = models.TextField()
    input_data = models.TextField(null=True,blank=True)
    output_data = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


class topic(models.Model):
    title = models.CharField(max_length = 150)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    
class problemset(models.Model):
    title = models.CharField(max_length=160)
    description = models.TextField()
    topic = models.ForeignKey(topic, on_delete=models.CASCADE, related_name='problems')
    input_data = models.TextField(default="")  # predefined input for testing
    expected_output = models.TextField(default="")  