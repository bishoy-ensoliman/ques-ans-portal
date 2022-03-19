from django import forms


class ContactForm(forms.Form):
    sender_email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=255, required=True)
    body = forms.CharField(widget=forms.Textarea)
