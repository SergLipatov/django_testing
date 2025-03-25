from django.urls import reverse

HOME_URL = reverse("notes:home")
ADD_URL = reverse("notes:add")
SUCCESS_URL = reverse("notes:success")
LIST_URL = reverse("notes:list")

LOGIN_URL = reverse("users:login")
LOGOUT_URL = reverse("users:logout")
SIGNUP_URL = reverse("users:signup")


def detail_url(slug):
    return reverse("notes:detail", args=[slug])


def edit_url(slug):
    return reverse("notes:edit", args=[slug])


def delete_url(slug):
    return reverse("notes:delete", args=[slug])
