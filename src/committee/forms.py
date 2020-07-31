from django import forms
from committee.models import Committee

class CreateCommitteeForm(forms.ModelForm):

    class Meta:
        model = Committee
        fields = ['name', 'description', 'image', 'back_image', 'link']

class UpdateCommitteeForm(forms.ModelForm):

    class Meta:
        model = Committee
        fields = ['name', 'description', 'image', 'back_image' , 'link']

    def save(self, commit=True):
        committee = self.instance
        committee.name = self.cleaned_data['name']
        committee.description = self.cleaned_data['description']
        committee.link = self.cleaned_data['link']

        if self.cleaned_data['image']:
            committee.image = self.cleaned_data['image']

        if self.cleaned_data['back_image']:
            committee.image = self.cleaned_data['back_image']

        if commit:
            committee.save()
        return committee
