from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    img = models.ImageField(upload_to='avatars', default='avatars/default.png')
    is_verified_email = models.BooleanField(default = False)
    email = models.EmailField(unique = True)

class EmailVerification(models.Model):
    key = models.UUIDField(unique = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True)
    experation = models.DateTimeField()

    def send_verif_email(self):
        link = reverse('userapp:email_verif', kwargs={'email':self.user.email, 'key':self.key})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        message = f'Тыкни сюда {verification_link}'
        print(settings.EMAIL_HOST_USER)
        send_mail(
            subject='Email Verification Espire Shop',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently = True
        )