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

    def clean(self):
        if self.is_valid:
            if EventPost.objects.filter(title=self.cleaned_data["title"]):
                raise forms.ValidationError(
                    "That Title is already taken, try adding your institue or commitee name!"
                )


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

    def clean(self):
        if self.is_valid:
            if EventPost.objects.filter(title=self.cleaned_data["title"]):
                raise forms.ValidationError(
                    "That Title is already taken, try adding your institue or commitee name!"
                )
