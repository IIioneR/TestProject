from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.http import urlencode
from django.views import View
from django.views.generic import ListView

from test_set.models import Test, Question


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

    def get(self, request, pk, seq_nr):
        question = Question.objects.filter(test__id=pk, number=seq_nr).first()

        answers = [answer.text for answer in question.answers.all()]
        return render(request=request,
                      template_name='testrun.html',
                      context={
                          'question': question,
                          'answers': answers
                      }
                      )

    def post(self, request, pk, seq_nr):
        return HttpResponse("OK")
