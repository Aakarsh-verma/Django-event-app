from django import forms
from event.models import EventPost


class CreateEventPostForm(forms.ModelForm):
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
