from django.db import models
from datetime import date


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    question_large_text = models.TextField(max_length=1000, default='')
    pub_date = models.DateTimeField('date published', help_text="Please use the following format: <em>YYYY-MM-DD</em>.")


class Choice(models.Model):
    question = models.ForeignKey(Question, verbose_name='choice_to_question', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0, null=True, blank=True)


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Entry(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField(default=date.today)
    authors = models.ManyToManyField(Author)
    number_of_comments = models.IntegerField(default=0)
    number_of_pingbacks = models.IntegerField(default=0)
    rating = models.IntegerField(default=5)

    def __str__(self):
        return self.headline


class Notes(models.Model):
    title = models.CharField(max_length=124)
    text = models.TextField()
    reminder = models.DateField()
    category = models.ForeignKey('Categories', related_name='note_category', on_delete=models.CASCADE)


class Categories(models.Model):
    title = models.CharField(max_length=124)
