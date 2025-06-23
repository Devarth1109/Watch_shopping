# signals.py

from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_added
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(social_account_added)
def create_user_from_social_account(request, sociallogin, **kwargs):
    user_data = sociallogin.account.extra_data  # This contains user data from Google
    email = user_data.get('email')
    
    # Check if the user already exists
    if not User.objects.filter(email=email).exists():
        User.objects.create(
            usertype='customer',  # Or however you want to define usertype
            fname=user_data.get('given_name', ''),
            lname=user_data.get('family_name', ''),
            email=email,
            pswd='',  # No password since this user logs in via Google
        )
