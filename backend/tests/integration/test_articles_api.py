from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class ArticleTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_article(self):
        data = {
            'title': 'Test Article',
            'description': 'This is a test article',
        }
        response = self.client.post('/api/articles/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['description'], data['description'])

    def test_get_articles(self):
        data = {
            'title': 'Test Article',
            'description': 'This is a test article',
        }
        self.client.post('/api/articles/', data, format='json')
        response = self.client.get('/api/articles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], data['title'])
        self.assertEqual(response.data[0]['description'], data['description'])

    def test_get_article(self):
        data = {
            'title': 'Test Article',
            'description': 'This is a test article',
        }
        response = self.client.post('/api/articles/', data, format='json')
        article_id = response.data['id']
        response = self.client.get(f'/api/articles/{article_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['description'], data['description'])

    def test_update_article(self):
        data = {
            'title': 'Test Article',
            'description': 'This is a test article',
        }
        response = self.client.post('/api/articles/', data, format='json')
        article_id = response.data['id']
        data['title'] = 'Updated Test Article'
        response = self.client.put(f'/api/articles/{article_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])
        self.assertEqual(response.data['description'], data['description'])

    def test_delete_article(self):
        data = {
            'title': 'Test Article',
            'description': 'This is a test article',
        }
        response = self.client.post('/api/articles/', data, format='json')
        article_id = response.data['id']
        response = self.client.delete(f'/api/articles/{article_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
