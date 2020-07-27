from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.template.defaultfilters import urlencode
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from django.conf import settings
from user_account.forms import UserAccountRegistrationForm, UserAccountProfileForm
from user_account.models import User


class CreateUserAccountView(CreateView):
    model = settings.AUTH_USER_MODEL
    template_name = 'registration.html'
    form_class = UserAccountRegistrationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register new user'
        return context

    def get_success_url(self):
        return reverse('index')


class UserAccountLoginView(LoginView):
    template_name = 'login.html'
    extra_context = {'title': 'Login as a user'}


class UserAccountLogoutView(LogoutView):
    template_name = 'logout.html'
    extra_context = {'title': 'Logout'}


class UserAccountProfileView(UpdateView):
    template_name = 'profile.html'
    extra_context = {'title': 'Edit current user profile'}
    form_class = UserAccountProfileForm

    def get_success_url(self):
        return reverse('index')

    def get_object(self, queryset=None):
        return self.request.user


class LeaderBoardListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'leaders_list.html'
    context_object_name = 'leaders_list'
    login_url = reverse_lazy('account:login')

    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().order_by('-avr_score')
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Leader Board'
        return context
