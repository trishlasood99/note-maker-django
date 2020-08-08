from django.db import models
from users.models import user
# Create your models here.
class FollowRequest(models.Model):
    from_user=models.ForeignKey(user,on_delete=models.CASCADE,related_name='requests_sent')
    to_user=models.ForeignKey(user,on_delete=models.CASCADE,related_name='requests_received')
    from_user_pk=models.IntegerField()
    date_sent=models.DateTimeField(auto_now_add=True)
    #message=models.TextField(blank=True)

    @classmethod
    def create(cls,to_user,from_user,from_user_pk):
        follow_request=cls(from_user=from_user,to_user=to_user,from_user_pk=from_user_pk)
        return follow_request


class Follower(models.Model):
    current_user=models.ForeignKey(user,on_delete=models.CASCADE,related_name='owner')
    followers=models.ManyToManyField(user)

    @classmethod
    def makeFollower(cls,current_user,new_friend):
        sender,created=cls.objects.get_or_create(current_user=current_user)
        sender.followers.add(new_friend)
        # receiver,created=cls.objects.get_or_create(
        # current_user=new_friend;
        # )
        # receiver.followers.add(current_user)
    #to establish a 2way relationship
    @classmethod
    def deleteFollower(cls,current_user,follower_to_remove):
        user1=cls.objects.get(current_user=current_user)
        user1.followers.remove(follower_to_remove)

    def __str__(self):
        return str(self.current_user)
