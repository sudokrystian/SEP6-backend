from django.http import HttpResponse
from django.contrib.auth.models import User

def authenticate_custom(username=None, password=None):
    try:
        valid_user = User.objects.get(username=username)
        if(valid_user):
            print("Valid login " + valid_user.password)
            if(password == valid_user.password):
                print("Valid password " + valid_user.password)
                return valid_user
            else:
                return None
    except User.DoesNotExist:
        return None