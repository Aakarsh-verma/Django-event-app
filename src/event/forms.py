from django import forms
from event.models import EventPost, EventCategory

choices = EventCategory.objects.all().values_list("name", "name")
choice_list = []
for item in choices:
    choice_list.append(item)


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
            "premium_applied": forms.CheckboxInput(attrs={"class": "form-check"}),
        }

    def clean(self):
        if self.is_valid:
            if self.cleaned_data["event_date"] < self.cleaned_data["reg_to"]:
                raise forms.ValidationError("Invalid Dates")


class UpdateEventPostForm(forms.ModelForm):
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
            "premium_applied": forms.CheckboxInput(attrs={"class": "form-check"}),
        }

    def clean(self):
        if self.is_valid:
            if self.cleaned_data["event_date"] < self.cleaned_data["reg_to"]:
                raise forms.ValidationError("Invalid Dates")


class ApplyPremiumForm(forms.ModelForm):
    premium_applied = forms.CharField(
        max_length=100, widget=forms.CheckboxInput(attrs={"class": "form-check"})
    )

    class Meta:
        model = EventPost
        fields = ["premium_applied"]


class ApprovePremiumForm(forms.ModelForm):
    premium_aproved = forms.CharField(
        max_length=100, widget=forms.CheckboxInput(attrs={"class": "form-check"})
    )
    priority = forms.IntegerField(
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = EventPost
        fields = ["premium_aproved", "priority"]

