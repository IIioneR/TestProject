from django.core.exceptions import ValidationError
from django.forms import ModelForm, BaseInlineFormSet

from test_set.models import Test, Question


class TestForm(ModelForm):
    model = Test

    class Meta:
        fields = '__all__'

    def clean(self):
        pass


class QuestionsInlineFormSet(BaseInlineFormSet):

    def clean(self):
        if not self.instance.MIN_LIMIT <= len(self.forms) <= self.instance.MAX_LIMIT:
            raise ValidationError('Quantity of question is out of range[{}..{}]'.format(
                self.instance.MIN_LIMIT, self.instance.MAX_LIMIT
            ))


class AnswerInlineFormSet(BaseInlineFormSet):

    def clean(self):
        if not self.instance.MIN_LIMIT <= len(self.forms) <= self.instance.MAX_LIMIT:
            raise ValidationError('Quantity of question is out of range[{}..{}]'.format(
                self.instance.MIN_LIMIT, self.instance.MAX_LIMIT
            ))
        correct_list = [
            form.cleaned_data['is_correct']
            for form in self.forms
        ]

        if not any(correct_list):
            raise ValidationError('you should select one correct answer')

        if all(correct_list):
            raise ValidationError("can't be all correct choises")
