from django.contrib import admin
from .models import FollowRequest, Follower
# Register your models here.
admin.site.register(FollowRequest)
admin.site.register(Follower)
