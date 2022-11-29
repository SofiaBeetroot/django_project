from django import forms
from api.models import Question


class QuestionForm(forms.Form):
    question_text = forms.CharField(label='Your question?', max_length=200)
    question_large_text = forms.CharField(widget=forms.Textarea)
    pub_date = forms.DateTimeField()


class QuestionModelFrom(forms.ModelForm):
    class Meta:
        model = Question
        exclude = ('id', )
