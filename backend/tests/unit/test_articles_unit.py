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

        self.assertEqual(data['title'], self.article.title)
        self.assertEqual(data['description'], self.article.description)

