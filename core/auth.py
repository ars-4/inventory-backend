from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


def get_or_create_token(user):
    token_found = False
    token = ""
    for tkn in Token.objects.all():
        if tkn.user == user:
            token_found = True
            token = tkn.key
    
    if token_found:
        return token
    
    else:
        token = Token.objects.create(
            user=user
        )
        token.save()
        return token.key
        