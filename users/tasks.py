from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery import shared_task
from django.conf import settings

@shared_task
def send_email_confirmation(user_id, uid, user_email):
    url = f'{settings.EMAIL_REDIRECT_DOMAIN}/users/email-confirmation/{user_id}/?uuid={uid}'
    subject = 'PixelCardWallet | Подтверждение email'
    html_content = render_to_string('email_confirmation.html', {'conf_link': url})
    msg = EmailMultiAlternatives(subject=subject, from_email=settings.EMAIL_HOST_USER, to=[user_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# разгружаем ну очень тяжелый запрос
@shared_task
def account_activate(user_id):
    from users.models.users import User

    user = User.objects.get(id=user_id)
    user.is_active=True
    user.save()