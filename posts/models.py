from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50, null=False)
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    view_count = models.IntegerField(default=0)
    image = models.ImageField(upload_to='images/', null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    like_user_set = models.ManyToManyField(User,
                                            blank=True,
                                            related_name='like_user_set',
                                            through='Like')
    # like_user_set = 모델과 다대다 관계를 형성하는데(이때 settings의 user model 과 관계를 이루고, 기본값에 공백을 가질 수 있고, 연관된 이름은 'like_user_set', Like 모델을 통해서 형성된다.)
    
    @property
    # get method를 표현
    def like_count(self):
        return self.like_user_set.count()
    # 좋아요 갯수를 세는 함수

class Comment(models.Model):
    content = models.TextField()
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 함께 가져 와서 고유해야하는 필드 이름 세트
    class Meta:
        unique_together = (('user','post'))
