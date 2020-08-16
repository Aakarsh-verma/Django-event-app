from django import forms
from blog.models import BlogPost, Category
from event.models import EventPost

choices = Category.objects.all().values_list("name", "name")
choice_list = []
for item in choices:
    choice_list.append(item)


class CreateBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "category", "body", "related_event", "image"]

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
            "related_event": forms.Select(attrs={"class": "form-control"}),
        }


class UpdateBlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "category", "body", "related_event", "image"]

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
            "related_event": forms.Select(attrs={"class": "form-control"}),
        }
