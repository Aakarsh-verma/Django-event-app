from django import forms
from blog.models import BlogPost, Category
from event.models import EventPost
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _


# 1MB - 1048576
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "1048576"

choices = Category.objects.all().values_list("name", "name")
choice_list = []
for item in choices:
    choice_list.append(item)


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "category", "body", "image", "related_event"]

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title.."}
            ),
            "category": forms.Select(
                choices=choice_list, attrs={"class": "form-control"}
            ),
            "body": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Content.."}
            ),
        }

    def clean(self, *args, **kwargs):
        if self.cleaned_data["image"]:
            self.check_file()
        if self.is_valid:
            if EventPost.objects.filter(title=self.cleaned_data["title"]):
                raise forms.ValidationError(
                    "That Title is already taken, try adding your institue or commitee name!"
                )

    def check_file(self, *args, **kwargs):
        image = self.cleaned_data["image"]
        content_type = image.content_type.split("/")[0]
        if image.size > int(MAX_UPLOAD_SIZE):
            raise forms.ValidationError(
                _("Please keep image size under %s. Current file size %s")
                % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(image.size),)
            )

        return image


class UpdateBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "category", "body", "image", "related_event"]

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title.."}
            ),
            "category": forms.Select(
                choices=choice_list, attrs={"class": "form-control"}
            ),
            "body": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Content.."}
            ),
        }

    def clean(self, *args, **kwargs):
        if self.cleaned_data["image"]:
            self.check_file()
        if self.is_valid:
            if EventPost.objects.filter(title=self.cleaned_data["title"]):
                raise forms.ValidationError(
                    "That Title is already taken by an event post,if its related to your event kindly add in the required field and try specifying!"
                )

    def check_file(self, *args, **kwargs):
        image = self.cleaned_data["image"]
        content_type = image.content_type.split("/")[0]
        if image.size > int(MAX_UPLOAD_SIZE):
            raise forms.ValidationError(
                _("Please keep image size under %s. Current file size %s")
                % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(image.size),)
            )

        return image

