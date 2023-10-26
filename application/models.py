from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _

def upload_to(instance, filename):
    return 'resumes/{filename}'.format(filename=filename)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Application(models.Model):

    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset()

    
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, default=1)
    jobid = models.CharField(max_length=250,default=1)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    resume = models.FileField(("Resume"), upload_to=upload_to, default='resumes/default.txt')
    coverletter = models.TextField(null=True)
    published = models.DateTimeField(default=timezone.now)
    

    objects = models.Manager()  # default manager
    postobjects = PostObjects()  # custom manager

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.name
    