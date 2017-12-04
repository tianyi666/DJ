from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.core.files.storage import FileSystemStorage

# fs = FileSystemStorage(location='/media/photos')
# class Car(models.Model):
#     photo = models.ImageField(storage=fs) #无视MEDIA_ROOT

from Dj666.system.storage import ImageStorage

class Dog(models.Model):
    name=models.CharField(max_length=50)
    # headimg = models.ImageField(upload_to='vft')
    headimg=models.ImageField(upload_to='vft',storage=ImageStorage())
    def get_absolute_url(self):
        return reverse_lazy('vft:dogdetails',kwargs={'pk':self.pk})

    def __str__(self):
        return self.name


SEX=(
    (1,'男'),
    (0,'女'),
)

class Panda(models.Model):
    name=models.CharField(max_length=20)
    age=models.IntegerField()
    sex=models.IntegerField(choices=SEX)
    desc=models.CharField(max_length=20)
    country=models.CharField(max_length=20)

    def modelprename(self):
        return 'pre' + self.name
    modelprename.short_description = 'Model定义的别名'

    class Meta:
        verbose_name='熊猫'

    def __str__(self):
        return self.name
