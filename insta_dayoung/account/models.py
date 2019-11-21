from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=15, help_text="최대 15자 입력 가능")
    image = models.ImageField(upload_to="images/", blank=True)
    follow_set = models.ManyToManyField('self', blank=True, through='Relation', symmetrical=False,)
    introduction = models.TextField(blank=True)

    @property
    def get_follower(self):
        return [i.from_user for i in self.follower_user.all()]

    @property
    def get_following(self):
        return [i.to_user for i in self.follow_user.all()]

    @property
    def follower_count(self):
        return len(self.get_follower)

    @property
    def following_count(self):
        return len(self.get_following)

    def is_follower(self, user):
        return user in self.get_follower

    def is_following(self, user):
        return user in self.get_following

    def __str__(self):
        return self.name

class Relation(models.Model):
    from_user = models.ForeignKey(User, related_name='follow_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='follower_user', on_delete=models.CASCADE)
    create_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{} -> {}".format(self.from_user, self.to_user)
    class Meta:
        unique_together = (('from_user', 'to_user'))
