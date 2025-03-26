from django.urls import reverse

HOME_URL = reverse("notes:home")
ADD_URL = reverse("notes:add")
SUCCESS_URL = reverse("notes:success")
LIST_URL = reverse("notes:list")

LOGIN_URL = reverse("users:login")
LOGOUT_URL = reverse("users:logout")
SIGNUP_URL = reverse("users:signup")


def get_redirect_url(destination_url):
    return f"{LOGIN_URL}?next={destination_url}"


REDIRECT_ADD_URL = get_redirect_url(ADD_URL)
REDIRECT_LIST_URL = get_redirect_url(LIST_URL)
REDIRECT_SUCCESS_URL = get_redirect_url(SUCCESS_URL)
