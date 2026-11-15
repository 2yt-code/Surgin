from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

# TODO
@receiver(reset_password_token_created)
def password_reset_token_created(
    sender,
    instance,
    reset_password_token,
    *args,
    **kwargs,
):
    user = reset_password_token.user

    send_mail(
        subject=_('Reset Password'),
        message=_(f'Your token for reset password: {reset_password_token.key}'),
        from_email=None,
        recipient_list=[user.email],
    )
