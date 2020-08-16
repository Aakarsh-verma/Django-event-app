from django.db import models

from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver


def upload_location(instance, filename, **kwargs):
    file_path = "committee/{author_id}/{name}-{filename}".format(
        author_id=str(instance.author.id), name=str(instance.name), filename=filename
    )
    return file_path


class Committee(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(max_length=5000, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)
    wallpaper = models.ImageField(upload_to=upload_location, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="date created")
    link = models.URLField(null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.name


@receiver(post_delete, sender=Committee)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)
    instance.wallpaper.delete(False)


def pre_save_commmitee_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)


pre_save.connect(pre_save_commmitee_post_receiver, sender=Committee)
