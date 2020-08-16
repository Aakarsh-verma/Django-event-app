from django import forms
from event.models import EventPost, EventCategory

choices = EventCategory.objects.all().values_list("name", "name")
choice_list = []
for item in choices:
    choice_list.append(item)

choices_list2 = [("Apply Now", "Apply Now"), ("Not Now", "Not Now")]


class CreateEventPostForm(forms.ModelForm):
    class Meta:
        model = EventPost
        fields = [
            "title",
            "category",
            "body",
            "reg_to",
            "event_date",
            "fee",
            "reg_link",
            "premium_applied",
            "image",
        ]

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
            "fee": forms.NumberInput(attrs={"class": "form-control"}),
            "reg_link": forms.URLInput(attrs={"class": "form-control"}),
            "premium_applied": forms.Select(
                choices=choices_list2, attrs={"class": "form-control"}
            ),
        }

    def clean(self):
        if self.is_valid:
            if self.cleaned_data["event_date"] < self.cleaned_data["reg_to"]:
                raise forms.ValidationError("Invalid Dates")


"""
    def save(self, commit=True):
        event_post = self.instance
        event_post.title = self.cleaned_data["title"]
        event_post.body = self.cleaned_data["body"]
        event_post.category = self.cleaned_data["category"]
        event_post.reg_to = self.cleaned_data["reg_to"]
        event_post.event_date = self.cleaned_data["event_date"]
        event_post.fee = self.cleaned_data["fee"]
        event_post.premium_applied = self.cleaned_data["premium_applied"]
        event_post.reg_link = self.cleaned_data["reg_link"]

        if self.cleaned_data["image"]:
            event_post.image = self.cleaned_data["image"]

        if commit:
            event_post.save()
        return event_post
"""


class UpdateEventPostForm(forms.ModelForm):
    class Meta:
        model = EventPost
        fields = [
            "title",
            "body",
            "category",
            "reg_to",
            "event_date",
            "fee",
            "reg_link",
            "premium_applied",
            "image",
        ]

    def clean(self):
        if self.is_valid:
            if self.cleaned_data["event_date"] < self.cleaned_data["reg_to"]:
                raise forms.ValidationError("Invalid Dates")

    def save(self, commit=True):
        event_post = self.instance
        event_post.title = self.cleaned_data["title"]
        event_post.body = self.cleaned_data["body"]
        event_post.category = self.cleaned_data["category"]
        event_post.reg_to = self.cleaned_data["reg_to"]
        event_post.event_date = self.cleaned_data["event_date"]
        event_post.fee = self.cleaned_data["fee"]
        event_post.premium_applied = self.cleaned_data["premium_applied"]
        event_post.reg_link = self.cleaned_data["reg_link"]

        if self.cleaned_data["image"]:
            event_post.image = self.cleaned_data["image"]

        if commit:
            event_post.save()
        return event_post
