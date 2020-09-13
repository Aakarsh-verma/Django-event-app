from django.db import models
from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.dispatch import receiver


def upload_location(instance, filename, **kwargs):
    file_path = "ad/{name}-{filename}".format(
        name=str(instance.name), filename=filename
    )
    return file_path


class AdPost(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    image = models.ImageField(null=False, blank=False, upload_to=upload_location)
    adlink = models.URLField(null=False, blank=False)

    def __str__(self):
        return self.name


@receiver(post_delete, sender=AdPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

