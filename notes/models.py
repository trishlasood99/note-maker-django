from django.db import models
from users.models import user
# Create your models here.
class Note(models.Model):
    user=models.ForeignKey(user,on_delete=models.CASCADE)
    contents=models.TextField(blank=True)
    title=models.CharField(max_length=50,default='Untitled')
    created=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)
    favourite=models.BooleanField(default=False)
    def __str__(self):
        return self.title

class SharedNote(models.Model):
    users=models.ManyToManyField(user,related_query_name='shared_note_participants')
    created_by=models.ForeignKey(user,on_delete=models.CASCADE,related_name='shared_note_creator')
    contents=models.TextField(blank=True)
    title=models.CharField(max_length=50,default='Untitled')
    created=models.DateTimeField(auto_now_add=True)
    last_modified=models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    # def limit_user_choices_to(self):
    #     followers_obj=Follower.objects.filter(current_user=self.created_by).first()
    #     if(followers_obj is None):
    #         return {'users':None}
    #     else:
    #         return {'users':followers_obj.followers.all()}
