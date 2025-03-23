# conftest.py
import pytest
from django.contrib.auth import get_user_model
from news.models import News, Comment
from datetime import datetime, timedelta


@pytest.fixture
def user(db):
    """Создает обычного пользователя."""
    return get_user_model().objects.create_user(
        username="testuser",
        password="password123"
    )


@pytest.fixture
def another_user(db):
    """Создает еще одного пользователя."""
    return get_user_model().objects.create_user(
        username="anotheruser",
        password="password123"
    )


@pytest.fixture
def author_client(client, user):
    """Клиент, который авторизован под пользователем `user`."""
    client.force_login(user)
    return client


@pytest.fixture
def news(db):
    """Создаёт тестовую новость."""
    return News.objects.create(
        title="Тестовая новость",
        text="Текст новости",
        date=datetime.today().date()
    )


@pytest.fixture
def create_news(db):
    """Создаёт несколько новостей для проверки списка новостей."""
    today = datetime.today().date()
    return News.objects.bulk_create([
        News(
            title=f"Новость {i}",
            text="Текст",
            date=today - timedelta(days=i)
        )
        for i in range(15)  # Создаём больше 10, чтобы проверить ограничение
    ])


@pytest.fixture
def comment(db, user, news):
    """Создаёт тестовый комментарий к новости от `user`."""
    return Comment.objects.create(
        news=news,
        author=user,
        text="Текст комментария"
    )


@pytest.fixture
def create_comments(db, user, news):
    """Создаёт несколько комментариев, чтобы проверить сортировку."""
    return Comment.objects.bulk_create([
        Comment(news=news, author=user, text=f"Комментарий {i}")
        for i in range(5)  # Создаём 5 комментариев
    ])


@pytest.fixture
def comment_data():
    """Возвращает данные для создания комментария."""
    return {"text": "Новый комментарий"}
