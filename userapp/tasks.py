from userapp.models import User
from django.utils.timezone import now
from userapp.models import EmailVerification
import uuid
from datetime import timedelta
from celery import shared_task


@shared_task
def celery_send_email_verif(user_id):
        user = User.objects.get(id=user_id)
        time_now = now()
        experation = time_now + timedelta(days=1)
        note = EmailVerification.objects.create(key=uuid.uuid4(), user=user, experation=experation)
        note.send_verif_email()
        note.save()