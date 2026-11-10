from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from .forms import RegisterForm

from .models import Post, Song

def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    songs = Song.objects.all().order_by('-release_date')
    return render(request, 'blog/home.html', {'posts': posts, 'songs': songs})

def about(request):
    return render(request, 'blog/about.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False  # can't login until email verified
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            link = f"http://127.0.0.1:8000/verify/{uid}/{token}/"

            send_mail(
                'Verify your IFOKONBALE account',
                f'Hi {user.username}, click here to verify: {link}',
                'noreply@ifokonbale.com',
                [user.email],
            )
            return render(request, 'blog/check_email.html')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'blog/verify_failed.html') 