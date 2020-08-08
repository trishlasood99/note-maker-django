from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class user(AbstractUser):
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=15,unique=True)
    email_id=models.EmailField()
    password=models.CharField(max_length=15)
    SECURITY_QUESTION_CHOICES=[
        (1,"What primary school did you attend?"),
        (2,"In what town or city did your mother and father meet?"),
        (3,"What is your mother's maiden name?"),
        (4,"What was your childhood pet's name?"),]
    security_question=models.IntegerField(choices=SECURITY_QUESTION_CHOICES,default=1)
    security_ans=models.CharField(max_length=15)
    REQUIRED_FIELDS=['first_name','last_name','password','email_id','security_question','security_ans']
    USERNAME_FIELD='username'
    EMAIL_FIELD='email_id'

    def __str__(self):
        return self.first_name+" "+self.last_name
