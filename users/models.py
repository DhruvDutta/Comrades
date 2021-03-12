from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q
class ProfileManager(models.Manager):

    def get_all_profiles_to_invite(self,sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        qs = Relationship.objects.filter(Q(sender=profile) | Q(receiver=profile))

        accepted = []
        for rel in qs:
            if rel.status == 'accepted':
                accepted.append(rel.receiver)
                accepted.append(rel.sender)
        available = [profile for profile in profiles if profile not in accepted]
        return available
    
    def get_all_profiles(self,me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    friends = models.ManyToManyField(User,related_name='friends',blank=True)
    objects = ProfileManager()
    def get_friends(self):
        return self.friends.all()
    
    def get_friends_no(self):
        return self.friends.all().count()
    
    


    def __str__(self):
        return str(self.user)

STATUS_CHOICES = (
    ('send','send'),
    ('accepted','accepted'),
)

class Relationshipmanager(models.Manager):
    def invitations_received(self,receiver):
        qs = Relationship.objects.filter(receiver=receiver,status='send')
        return qs

class Relationship(models.Model):
    sender = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='sender')
    receiver = models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='receiver')
    status = models.CharField(max_length=8,choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    objects = Relationshipmanager()
    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"

