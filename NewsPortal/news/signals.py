from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.db.models.signals import m2m_changed
from django.template.loader import render_to_string

from .models import PostCategory,Post
from NewsPortal import settings


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category_post.all()
        subscribers_email = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_email += [s.email for s in subscribers]
        send_notifications(instance.preview, instance.pk, instance.title, subscribers_email)


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'email_template.html',
        {
            'cat' : PostCategory.category_post,
            'text': preview,
            'link': f'{settings.SITE_URL}/posts/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
