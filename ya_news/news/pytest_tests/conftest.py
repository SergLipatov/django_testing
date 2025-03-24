import pytest

from django.conf import settings
from django.contrib.auth import get_user_model

from datetime import datetime, timedelta

from news.models import News, Comment

User = get_user_model()

NUM_TEST_COMMENTS = 5  # Количество тестовых комментариев


@pytest.fixture
def user_factory(db):
    """Фабрика пользователей."""
    def create_user(**kwargs):
        return User.objects.create(**kwargs)
    return create_user


@pytest.fixture
def user(user_factory):
    """Создает обычного пользователя."""
    return user_factory(username="testuser")


@pytest.fixture
def another_user(user_factory):
    """Создает еще одного пользователя."""
    return user_factory(username="anotheruser")


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
    news_count = settings.NEWS_COUNT_ON_HOME_PAGE + 1  # Берем из настроек
    today = datetime.today().date()
    return News.objects.bulk_create([
        News(
            title=f"Новость {i}",
            text="Текст",
            date=today - timedelta(days=i)
        )
        for i in range(news_count)
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
        for i in range(NUM_TEST_COMMENTS)
    ])


@pytest.fixture
def comment_data():
    """Возвращает данные для создания комментария."""
    return {"text": "Новый комментарий"}
