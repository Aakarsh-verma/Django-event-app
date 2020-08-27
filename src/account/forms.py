from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from .models import Account


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=254,
        help_text="Required. Add a valid email address.",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Account
        fields = (
            "email",
            "username",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"


class AccountAuthenticationForm(forms.ModelForm):

    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ("email", "password")

    def __init__(self, *args, **kwargs):
        super(AccountAuthenticationForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["class"] = "form-control"

    def clean(self):
        if self.is_valid:
            email = self.cleaned_data["email"]
            password = self.cleaned_data["password"]
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login")


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            "email",
            "username",
            "website_url",
            "facebook_url",
            "twitter_url",
            "instagram_url",
            "youtube_url",
        ]

        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "website_url": forms.URLInput(attrs={"class": "form-control"}),
            "facebook_url": forms.URLInput(attrs={"class": "form-control"}),
            "twitter_url": forms.URLInput(attrs={"class": "form-control"}),
            "instagram_url": forms.URLInput(attrs={"class": "form-control"}),
            "youtube_url": forms.URLInput(attrs={"class": "form-control"}),
        }

    def clean_email(self):
        if self.is_valid:
            email = self.cleaned_data["email"]
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % email)

    def clean_username(self):
        if self.is_valid:
            username = self.cleaned_data["username"]
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(
                    username=username
                )
            except:
                return username
            raise forms.ValidationError('Username "%s" is already in use.' % username)

