from django import forms

class SignForm(forms.Form):
	# name = forms.CharField(label='', widget=forms.HiddenInput)
	name = forms.CharField(label='')
	content = forms.CharField(label='', widget=forms.Textarea, max_length=1000)
