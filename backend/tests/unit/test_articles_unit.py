from django.test import TestCase
from core.serialziers import ArticleSerializer
from core.models import Article

class TestArticleSerializerUnit(TestCase):
    def setUp(self):
        self.article = Article.objects.create(
            title="Test Article",
            description="This is a test article"
        )

    def test_serialize_article(self):
        serializer = ArticleSerializer(self.article)
        data = serializer.data

        self.assertEqual(data['title'], 'Wrong Title')
        # self.assertEqual(data['title'], self.article.title)
        self.assertEqual(data['description'], self.article.description)

    def test_deserialize_article(self):
        data = {
            "title": "New Test Article",
            "description": "This is a new test article"
        }
        serializer = ArticleSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        article = serializer.save()
        self.assertEqual(article.title, data['title'])
        self.assertEqual(article.description, data['description'])

    def test_update_article(self):
        data = {
            "title": "Updated Test Article",
            "description": "This is an updated test article"
        }
        serializer = ArticleSerializer(self.article, data=data)
        self.assertTrue(serializer.is_valid())

        article = serializer.save()
        self.assertEqual(article.title, data['title'])
        self.assertEqual(article.description, data['description'])

    def test_delete_article(self):
        self.article.delete()
        self.assertFalse(Article.objects.filter(id=self.article.id).exists())

