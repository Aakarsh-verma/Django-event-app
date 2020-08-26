from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from event.models import EventPost, EventCategory, Profile
from account.models import Account


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

choices = EventCategory.objects.all().values_list("name", "name")
choice_list = []
for item in choices:
    choice_list.append(item)


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["user", "profile_pic"]

        widgets = {
            "user": forms.TextInput(attrs={"class": "form-control", "hidden": "True"})
        }


class AddSocialLinksForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = (
            "website_url",
            "facebook_url",
            "twitter_url",
            "instagram_url",
            "youtube_url",
        )

    def __init__(self, *args, **kwargs):
        super(AddSocialLinksForm, self).__init__(*args, **kwargs)

        self.fields["website_url"].widget.attrs["class"] = "form-control"
        self.fields["facebook_url"].widget.attrs["class"] = "form-control"
        self.fields["twitter_url"].widget.attrs["class"] = "form-control"
        self.fields["instagram_url"].widget.attrs["class"] = "form-control"
        self.fields["youtube_url"].widget.attrs["class"] = "form-control"


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["profile_pic"]

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

        self.fields["profile_pic"].widget.attrs["class"] = "form-check"

    def clean(self, *args, **kwargs):
        if self.cleaned_data["profile_pic"]:
            self.check_file()
        return self.cleaned_data

    def check_file(self, *args, **kwargs):
        profile_pic = self.cleaned_data["profile_pic"]
        content_type = profile_pic.content_type.split("/")[0]
        if profile_pic.size > int(MAX_UPLOAD_SIZE):
            raise forms.ValidationError(
                _("Please keep image size under %s. Current file size %s")
                % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(profile_pic.size),)
            )

        return profile_pic


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

    def clean(self, *args, **kwargs):
        if self.cleaned_data["image"]:
            self.check_file()
        if self.is_valid:
            if self.cleaned_data["event_date"] < self.cleaned_data["reg_to"]:
                raise forms.ValidationError("Invalid Registration Dates")

    def check_file(self, *args, **kwargs):
        image = self.cleaned_data["image"]
        content_type = image.content_type.split("/")[0]
        if image.size > int(MAX_UPLOAD_SIZE):
            raise forms.ValidationError(
                _("Please keep image size under %s. Current file size %s")
                % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(image.size),)
            )

        return image


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

    def clean(self, *args, **kwargs):
        if self.cleaned_data["image"]:
            self.check_file()
        if self.is_valid:
            if self.cleaned_data["event_date"] < self.cleaned_data["reg_to"]:
                raise forms.ValidationError("Invalid Dates")

    def check_file(self, *args, **kwargs):
        image = self.cleaned_data["image"]
        content_type = image.content_type.split("/")[0]
        if image.size > int(MAX_UPLOAD_SIZE):
            raise forms.ValidationError(
                _("Please keep image size under %s. Current file size %s")
                % (filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(image.size),)
            )

        return image


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

