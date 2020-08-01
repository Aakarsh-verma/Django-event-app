from django.db import models

from django.db.models.signals import pre_save, post_delete
from django.utils.text import slugify
from django.conf import settings
from django.dispatch import receiver


def upload_location(instance, filename, **kwargs):
    file_path = "event/{author_id}/{title}-{filename}".format(
        author_id=str(instance.author.id), title=str(instance.title), filename=filename
    )
    return file_path


class EventPost(models.Model):
    CATEGORY_CHOICE = [
        ("COMP/IT", "Computer"),
        ("EXTC/ETRX", "Electrical"),
        ("MECH/AUTO", "Mechanical"),
        ("ALL", "All"),
        ("NON-TECH", "Non-Technical"),
        ("", ""),
    ]

    title = models.CharField(max_length=50, null=False, blank=False)
    body = models.TextField(max_length=5000, null=False, blank=False)
    image = models.ImageField(upload_to=upload_location, default="pce_logo.png")
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICE, default="All")
    category2 = models.CharField(max_length=10, choices=CATEGORY_CHOICE, default="")
    event_date = models.DateField(
        auto_now_add=False, null=False, blank=False, verbose_name="event date"
    )
    reg_to = models.DateField(
        auto_now_add=False, null=False, blank=False, verbose_name="registration to"
    )
    fee = models.PositiveIntegerField(default=0)
    reg_link = models.URLField(null=False, blank=False)
    date_published = models.DateTimeField(
        auto_now_add=True, verbose_name="date published"
    )
    date_updated = models.DateTimeField(auto_now=True, verbose_name="date updated")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title


@receiver(post_delete, sender=EventPost)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_event_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.author.username + "-" + instance.title)


pre_save.connect(pre_save_event_post_receiver, sender=EventPost)
