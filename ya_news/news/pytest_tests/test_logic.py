# test_logic.py
from http import HTTPStatus

import pytest
from django.urls import reverse
from news.models import Comment

BAD_WORDS = ('редиска', 'негодяй')
WARNING = 'Не ругайтесь!'


def test_anonymous_user_cannot_comment(client, news, comment_data):
    """Анонимный пользователь не может отправить комментарий."""
    url = reverse('news:detail', args=[news.pk])
    response = client.post(url, data=comment_data)

    assert Comment.objects.count() == 0
    assert response.status_code == HTTPStatus.FOUND


def test_authorized_user_can_comment(author_client, news, comment_data):
    """Авторизованный пользователь может отправить комментарий."""
    url = reverse('news:detail', args=[news.pk])
    response = author_client.post(url, data=comment_data)

    assert Comment.objects.count() == 1
    assert response.status_code == HTTPStatus.FOUND


@pytest.mark.parametrize("bad_word", BAD_WORDS)
def test_prohibited_words_in_comment(author_client, news, bad_word):
    """Запрещённые слова в комментариях не допускаются."""
    url = reverse('news:detail', args=[news.pk])
    response = author_client.post(url, data={'text': f'Это {bad_word}!'})

    assert Comment.objects.count() == 0
    assert WARNING.encode() in response.content


def test_user_can_edit_own_comment(author_client, comment):
    """Авторизованный пользователь может редактировать свои комментарии."""
    url = reverse('news:edit', args=[comment.pk])
    new_text = "Обновленный комментарий"
    response = author_client.post(url, data={'text': new_text})

    comment.refresh_from_db()
    assert comment.text == new_text
    assert response.status_code == HTTPStatus.FOUND


def test_user_cannot_edit_others_comment(author_client, another_user, comment):
    """Пользователь не может редактировать чужие комментарии."""
    author_client.force_login(another_user)
    url = reverse('news:edit', args=[comment.pk])
    response = author_client.post(url, data={'text': 'Мой новый текст'})

    comment.refresh_from_db()
    assert comment.text != 'Мой новый текст'
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_user_can_delete_own_comment(author_client, comment):
    """Авторизованный пользователь может удалять свои комментарии."""
    url = reverse('news:delete', args=[comment.pk])
    response = author_client.post(url)

    assert not Comment.objects.filter(pk=comment.pk).exists()
    assert response.status_code == HTTPStatus.FOUND


def test_user_cannot_delete_others_comment(
        author_client,
        another_user,
        comment
):
    """Пользователь не может удалять чужие комментарии."""
    author_client.force_login(another_user)
    url = reverse('news:delete', args=[comment.pk])
    response = author_client.post(url)

    assert Comment.objects.filter(pk=comment.pk).exists()
    assert response.status_code == HTTPStatus.NOT_FOUND
