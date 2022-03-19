from django.shortcuts import render, redirect
from django.core.mail import mail_admins
from . import forms


# Create your views here.
def contact(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            mail_admins(form.cleaned_data.get('subject'),
                        "Sender: " + form.cleaned_data.get('sender_email') + '\n'
                        + form.cleaned_data.get('body'),
                        fail_silently=False)
            return redirect('questions:index')
    else:
        form = forms.ContactForm()
    return render(request, 'contact/contact_form.html', {'form': form})


def download(request):
    return render(request, 'contact/download_app.html')