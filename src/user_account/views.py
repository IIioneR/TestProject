from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.template.defaultfilters import urlencode
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView, FormView

from django.conf import settings
from user_account.forms import UserAccountRegistrationForm, UserAccountProfileForm, ContactUs
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
    ordering = ['-avr_score']

    paginate_by = 10

    # def get_queryset(self):
    #     qs = super().get_queryset().order_by('avr_score')
    #     return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['title'] = 'Leader Board'
        return context


class ContactUsView(FormView):
    template_name = 'contact_us.html'
    extra_context = {'title': 'Send us a message!'}
    success_url = reverse_lazy('index')
    form_class = ContactUs

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            send_mail(
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message'],
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
