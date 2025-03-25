import datetime

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse

from news.models import News, Comment

User = get_user_model()
NUM_TEST_COMMENTS = 5


@pytest.fixture
def user(db):
    """Создаёт тестового пользователя."""
    return User.objects.create(username="testuser")


@pytest.fixture
def another_user(db):
    """Создаёт ещё одного тестового пользователя."""
    return User.objects.create(username="anotheruser")


@pytest.fixture
def author_client(db, user):
    """Создаёт клиент с авторизованным пользователем."""
    client = Client()
    client.force_login(user)
    return client


@pytest.fixture
def another_author_client(db, another_user):
    """Создаёт клиент с авторизованным другим пользователем."""
    client = Client()
    client.force_login(another_user)
    return client


@pytest.fixture
def news(db):
    """Создаёт одну тестовую новость."""
    return News.objects.create(
        title="Тестовая новость",
        text="Текст новости",
        date=datetime.date.today()
    )


@pytest.fixture
def news_list(db):
    """Создаёт список новостей."""
    today = datetime.date.today()
    news = []

    for i in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1):
        news_item = News.objects.create(
            title=f"Новость {i}",
            text="Текст",
            date=today - datetime.timedelta(days=i)
        )
        news.append(news_item)

    return news


@pytest.fixture
def comment(db, user, news):
    """Создаёт комментарий одного пользователя к одной новости."""
    return Comment.objects.create(
        news=news,
        author=user,
        text="Тестовый комментарий"
    )


@pytest.fixture
def comments(db, user, news):
    """Создаёт несколько комментариев с разными датами."""
    comments = []
    for i in range(NUM_TEST_COMMENTS):
        created_date = datetime.datetime.now() - datetime.timedelta(days=i)
        comment = Comment(news=news, author=user, text=f"Комментарий {i}")
        comment.save()
        Comment.objects.filter(id=comment.id).update(created=created_date)
        comments.append(
            Comment.objects.get(id=comment.id))
    return comments


@pytest.fixture
def home_url():
    """URL для главной страницы новостей."""
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    """URL для детальной страницы одной новости."""
    return reverse('news:detail', args=[news.pk])


@pytest.fixture
def edit_url(comment):
    """URL для редактирования комментария."""
    return reverse('news:edit', args=[comment.pk])


@pytest.fixture
def delete_url(comment):
    """URL для удаления комментария."""
    return reverse('news:delete', args=[comment.pk])


@pytest.fixture
def login_url():
    """URL для страницы логина."""
    return reverse('users:login')


@pytest.fixture
def logout_url():
    """URL для страницы выхода."""
    return reverse('users:logout')


@pytest.fixture
def signup_url():
    """URL для страницы регистрации."""
    return reverse('users:signup')
