import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Max, Sum
from django.http import HttpResponse, HttpResponseNotAllowed
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

    def get(self, request, pk):
        if 'testresult' not in request.session:
            return HttpResponseNotAllowed('ERROR')

        testresult_step = request.session.get('testresult_step', 1)

        request.session['testresult_step'] = testresult_step

        question = Question.objects.get(test__id=pk, number=testresult_step)

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

    def post(self, request, pk):
        if 'testresult_step' not in request.session:
            return HttpResponseNotAllowed('ERROR')

        testresult_step = request.session['testresult_step']

        test = Test.objects.get(pk=pk)
        question = Question.objects.get(test__id=pk, number=testresult_step)

        answers = Answer.objects.filter(
            question=question
        ).all()

        choices = {
            k.replace(self.PREFIX, ''): True
            for k in request.POST if k.startswith(self.PREFIX)
        }

        if not choices:
            messages.error(self.request, extra_tags='danger', message="ERROR: You should select at least 1 answer!")
            return redirect(reverse('tests:next', kwargs={'pk': pk, 'seq_nr': testresult_step}))

        current_test_result = TestResult.objects.get(id=request.session['testresult'])

        for idx, answer in enumerate(answers, 1):
            value = choices.get(str(idx), False)
            TestResultDetail.objects.create(
                test_result=current_test_result,
                question=question,
                answer=answer,
                is_correct=(value == answer.is_correct)
            )

        if question.number < test.questions_count():
            current_test_result.is_new = False
            current_test_result.save()
            request.session['testresult_step'] = testresult_step + 1
            return redirect(reverse('tests:next', kwargs={'pk': pk}))
        else:
            current_test_result.finish()
            current_test_result.save()
            questions_count = test.questions_count()
            return render(
                request=request,
                template_name='testrun_end.html',
                context={
                    'test_result': current_test_result,
                    'test': test,
                    'time_spent': datetime.datetime.utcnow() - current_test_result.datetime_run.replace(tzinfo=None),
                    'questions_count': questions_count,

                }
            )


class StartTestView(View):

    def get(self, request, pk):

        test = Test.objects.get(pk=pk)

        test_result_id = request.session.get('testresult')

        if test_result_id:
            test_result = TestResult.objects.get(id=test_result_id)
        else:
            test_result = TestResult.objects.create(
                user=request.user,
                test=test
            )

        request.session['testresult'] = test_result.id

        qs = TestResult.objects.all()

        question_count = test.questions_count

        number_runs = test.test_results.count()
        best_r = qs.aggregate(Max('avr_score')).get('avr_score__max')
        best_user_r = TestResult.objects.filter(avr_score=best_r).first().user.get_username()

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
