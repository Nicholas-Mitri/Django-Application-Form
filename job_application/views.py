from django.shortcuts import render

from mysite.settings import EMAIL_HOST_USER
from .forms import ApplicationForm
from .models import Form
from django.contrib import messages
from django.core.mail import EmailMessage


def index(request):
    """
    View function for handling job application form submissions.

    Renders the job application form page and processes form submissions.
    If the form is submitted via POST and is valid, it:
    1. Saves the application data to the database
    2. Sends a confirmation email to the admin
    3. Displays a success message to the user

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse object with the rendered index.html template
    """
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            date = form.cleaned_data["date"]
            occupation = form.cleaned_data["occupation"]

            Form.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                date=date,
                occupation=occupation,
            )

            message_body = f"A new application has been submitted:\n\n"
            message_body += f"First Name: {first_name}\nLast Name: {last_name}\nEmail: {email}\nDate: {date}\nOccupation: {occupation}"
            email_message = EmailMessage(
                subject="Form submission confirmation",
                body=message_body,
                to=[EMAIL_HOST_USER],
            )
            email_message.send()

            messages.success(request, "Form submitted successfully!")
    return render(request, "index.html")


def about(request):
    """
    View function for rendering the about page.

    Displays information about the company or organization.

    Args:
        request: HttpRequest object

    Returns:
        HttpResponse object with the rendered about.html template
    """
    return render(request, "about.html")
