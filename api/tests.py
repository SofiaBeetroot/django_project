import datetime
from django.test import TestCase, Client
from api.models import Entry, Blog, Author


class EntryTest(TestCase):
    def setUp(self) -> None:
        self.blog = Blog.objects.create(name='Test blog', tagline='We tested our app')
        self.author = Author.objects.create(name='Beetroot', email='beetroot@gmail.com')
        entry = Entry.objects.create(blog=self.blog, headline='Test entry', body_text='We tested our model',
                                     pub_date=datetime.datetime.now())
        entry_second = Entry.objects.create(blog=self.blog, headline='Test ENTRY', body_text='We tested our model',
                                            pub_date=datetime.datetime.now())
        entry.authors.set([self.author])
        entry_second.authors.set([self.author])

    def test_get_entry_object(self):
        entry = Entry.objects.get(headline='Test entry')
        self.assertEqual(str(entry), entry.headline)

    def test_get_entry_rating(self):
        entry = Entry.objects.get(headline='Test ENTRY')
        self.assertEqual(entry.get_rating(), 5)

    def test_get_entry_authors(self):
        entry = Entry.objects.get(headline='Test ENTRY')
        self.assertEqual(list(entry.get_author_list()), [self.author])


class AllViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_blog_view(self):
        response = self.client.get('/blogs')
        self.assertEqual(list(list(response.context)[0]['list']), list(Blog.objects.all()))

    def test_blog_content(self):
        response = self.client.get('/blogs')
        print(response.content_type)
