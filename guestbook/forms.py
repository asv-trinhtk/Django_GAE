from django import forms

class SignForm(forms.Form):
	guestbook_name = forms.CharField(label='', widget=forms.HiddenInput)
	content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows': 5}), max_length=10)

