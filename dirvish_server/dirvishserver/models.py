from django.db import models

# Create your models here.
class File(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    inode = models.IntegerField(null=True, blank=True)
    size = models.IntegerField(null=True, blank=True)
    type = models.IntegerField(null=True, blank=True)
    name = models.TextField(blank=True)
    class Meta:
        db_table = 'file'

class Image(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    name = models.TextField(blank=True)
    time = models.TextField(blank=True)
    class Meta:
        db_table = 'image'

class ImageFile(models.Model):
    image = models.ForeignKey(Image)
    # IntegerField(null=True, blank=True)
    file = models.ForeignKey(File)
    # IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'image_file'