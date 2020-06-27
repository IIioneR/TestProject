import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.http import urlencode
from django.views import View
from django.views.generic import ListView, DetailView

from test_set.models import Test, Question, TestResult, Answer, TestResultDetail


class TestListView(LoginRequiredMixin, ListView):
    model = Test
    template_name = 'tests_list.html'
    context_object_name = 'tests_list'
    login_url = reverse_lazy('account:login')
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        params = self.request.GET

        context['title'] = 'Test suites'
        context['query_params'] = urlencode({k: v for k, v in params.items() if k != 'page'})
        return context


class TestRunView(View):
    PREFIX = 'answer_'

    def get(self, request, pk, seq_nr):
        question = Question.objects.filter(test__id=pk, number=seq_nr).first()

        answers = [
            answer.text
            for answer in question.answers.all()
        ]

        return render(
            request=request,
            template_name='testrun.html',
            context={
                'question': question,
                'answers': answers,
                'prefix': self.PREFIX
            }
        )

    def post(self, request, pk, seq_nr):
        test = Test.objects.get(pk=pk)
        question = Question.objects.filter(test__id=pk, number=seq_nr).first()

        answers = Answer.objects.filter(
            question=question
        ).all()

        choices = {
            k.replace(self.PREFIX, ''): True
            for k in request.POST if k.startswith(self.PREFIX)
        }

        if not choices:
            messages.error(self.request, extra_tags='danger', message="ERROR: You should select at least 1 answer!")
            return redirect(reverse('tests:testrun_step', kwargs={'pk': pk, 'seq_nr': seq_nr}))

        current_test_result = TestResult.objects.filter(
            test=test,
            user=request.user,
            is_completed=False).last()

        for idx, answer in enumerate(answers, 1):
            value = choices.get(str(idx), False)
            TestResultDetail.objects.create(
                test_result=current_test_result,
                question=question,
                answer=answer,
                is_correct=(value == answer.is_correct)
            )

        if question.number < test.questions_count():
            return redirect(reverse('tests:testrun_step', kwargs={'pk': pk, 'seq_nr': seq_nr + 1}))
        else:
            current_test_result.finish()
            current_test_result.save()
            return render(
                request=request,
                template_name='testrun_end.html',
                context={
                    'test_result': current_test_result,
                    'test': test,
                    'time_spent': datetime.datetime.utcnow() - current_test_result.datetime_run.replace(tzinfo=None)
                }
            )


class StartTestView(View):

    def get(self, request, pk):
        qs = TestResult.objects.all()
        test = Test.objects.get(pk=pk)
        question_count = test.questions.count()
        number_runs = test.test_results.count()
        best_r = qs.aggregate(Max('avr_score')).get('avr_score')
        print(f'HEEEEEEEEEEEEERE{best_r}')
        best_user_r = [test.user.get_username()
                       for test in TestResult.objects.filter(avr_score=best_r)
                       ]
        test_result = TestResult.objects.create(
            user=request.user,
            test=test
        )

        return render(
            request=request,
            template_name='testrun_start.html',
            context={
                'test': test,
                'test_result': test_result,
                'question_count': question_count,
                'number_runs': number_runs,
                'best_r': best_r,
                'best_user_r': best_user_r
            },
        )
