from django.db import models
from django.contrib.auth.models import User

from scarlet.versioning import fields
from scarlet.versioning.models import VersionView, Cloneable
from scarlet.cms.fields import OrderField


class UserSite(models.Model):
    user = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE)
    data = models.IntegerField()


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return str(self.name)


class DummyModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class Category(VersionView):
    category = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, editable=False)

    def __str__(self):
        return self.category


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Post(VersionView):
    date = models.DateField()
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, editable=False)
    body = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = fields.M2MFromVersion(Tag, blank=True)
    # SEO Section
    keywords = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.title)


class PostImage(Cloneable):
    post = fields.FKToVersion(Post)
    caption = models.CharField(max_length=255, blank=True)
    order = OrderField()

    def __str__(self):
        return self.caption or str(self.image)


class Comment(VersionView):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return self.text[:20]


Post.register_related(related_name="postimage")
