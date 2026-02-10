from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import ExampleItem


class ExampleItemAPITest(APITestCase):
    def setUp(self):
        """Подготовка данных перед каждым тестом"""
        # Создаём пользователя
        self.user = User.objects.create_user(
            username='testuser',
            password='pass123'
        )
        # Авторизуем клиент
        self.client.login(username='testuser', password='pass123')

        # Создаём тестовую запись
        self.item = ExampleItem.objects.create(
            title="Старая задача",
            author=self.user
        )

    def test_can_list_items(self):
        """Проверка: можно получить список задач"""
        response = self.client.get('/api/items/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Старая задача')

    def test_can_create_item(self):
        """Проверка: можно создать новую задачу"""
        response = self.client.post('/api/items/', {
            'title': 'Новая задача'
        })
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ExampleItem.objects.count(), 2)
        self.assertEqual(ExampleItem.objects.last().title, 'Новая задача')
        self.assertEqual(response.data['author']['username'], 'testuser')

    def test_can_retrieve_single_item(self):
        """Проверка: можно получить одну задачу по ID"""
        response = self.client.get(f'/api/items/{self.item.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Старая задача')

    def test_can_update_own_item(self):
        """Проверка: автор может редактировать свою задачу"""
        response = self.client.patch(f'/api/items/{self.item.id}/', {
            'title': 'Обновлённая задача'
        })
        self.assertEqual(response.status_code, 200)
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, 'Обновлённая задача')

