from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.http import HttpResponse
from resume.settings import EMAIL_HOST_USER

# Create your views here.
def index(request):
    if request.method == 'GET':
        return render(request, 'my_resume/index.html', {'form': ContactForm()})
    else:
        try: 
            form = ContactForm(request.POST)
            if form.is_valid():
                body = {
                'name': f"<b>Name:</b> {form.cleaned_data['name']}", 
                'email': f"<b>Email: </b> {form.cleaned_data['email']}", 
                'title': f"<b>Title: </b>{form.cleaned_data['title']}", 
                'message': f"<b>Message: </b><br />{form.cleaned_data['message']}", 
                }
                name = form.cleaned_data['name']
                message = "<br />".join(body.values())
                subject = f"Message from {name}"
                email = EmailMessage(subject, message, to=[EMAIL_HOST_USER])
                email.content_subtype = "html"

            try:
                email.send()
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return render(request, 'my_resume/index.html', {"success": f"Thanks for your message {name}. I will get back to you soon."})
        except ValueError:
            return render(request, 'my_resume/index.html', {'form':ContactForm(), 'error':'Bad data passed in. Try again'})
