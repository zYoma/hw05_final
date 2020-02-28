from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

def gen_slug(slug):
    new_slug = slugify(slug, allow_unicode = True)
    return new_slug

class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=150, unique = True)
    description = models.TextField()
  
# Переопределим метод save, чтобы сгенерировать слаг, хоть это и не требуется по заданию.
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, related_name="post_group")
    image = models.ImageField(upload_to='posts/', null = True) 

    def __str__(self):
       # выводим текст поста 
       return self.text

class Comment(models.Model):
    text = models.TextField()
    created = models.DateTimeField("date published", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comment")

class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
