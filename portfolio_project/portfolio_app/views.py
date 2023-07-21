from django.shortcuts import render, redirect
from .models import Home, About, Profile, Category, Skills, Portfolio, Contact
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ContactForm
from django.conf import settings


def index(request):
    if request.method == "GET":

        # Home
        home = Home.objects.latest('updated')

        # About
        about = About.objects.latest('updated')
        profiles = Profile.objects.filter(about=about)

        # Skills
        categories = Category.objects.all()

        # Portfolio
        portfolios = Portfolio.objects.all()

        form = ContactForm()

        context = {
            'home': home,
            'about': about,
            'profiles': profiles,
            'categories': categories,
            'portfolios': portfolios,
            "form": form
        }

        return render(request, 'index.html', context)

    # Contact

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            name = form.cleaned_data.get("name")
            message = form.cleaned_data.get("message")

            Contact.objects.create(email=email, name=name, message=message)

            messages.success(
                request, f"Thank you for reaching out. We will get back to you!")
            
            # Sending email to myself
            email_subject = "You got a message from your live portfolio website"
            email_msg = f"Name : {name}\nEmail : {email}\nMesage : {message}"
            send_mail(subject=email_subject,message=email_msg,from_email=settings.EMAIL_HOST_USER,recipient_list=[settings.EMAIL_HOST_USER])

            return redirect("index")
