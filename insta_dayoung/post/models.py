from django.db import models
from django.conf import settings
from account.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill



# Create your models here.
class Post(models.Model):
    content = models.CharField(max_length=140, help_text="최대 140자 입력 가능")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # image = models.ImageField(upload_to="images/", blank=True)
    image = ProcessedImageField(upload_to="images/",
                                processors=[ResizeToFill(600, 600)],
                                format='JPEG',
                                options={'quality': 90})
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    like_user_set = models.ManyToManyField(User, blank=True, related_name='like_user_set', through='Like')
    hashtags = models.ManyToManyField('Hashtag', blank=True)
    # tag_set = models.ManyToManyField('Tag', blank=True)
    # like_user_set = models.ManyToManyField(settings.AUTH_USER_MODEL,
    #                                        blank=True,
    #                                        related_name='like_user_set',
    #                                        through='Like')  # post.like_set 으로 접근 가능
    class Meta: 
        ordering = ['-created_at']

    @property
    def like_count(self):
        return self.like_user_set.count()
        
    def index(self):
        return self.content[:50]

    
class Hashtag(models.Model):
    content = models.TextField(unique=True)
    def __str__(self):
        return self.content

class Like(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    diary = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
