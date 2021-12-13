from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic.base import RedirectView, TemplateView
from .forms import RegistrationForm, ProfileCreateForm
from django.contrib.auth.models import User
from .models import Profile
# Create your views here.


class SignupView(CreateView):
    form_class = RegistrationForm
    success_url = reverse_lazy('homepage')
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['profile_form'] = ProfileCreateForm(self.request.POST or None)
        print(context)
        return context

    def form_valid(self, form):
        profile_form = ProfileCreateForm(self.request.POST)
        if profile_form.is_valid():
            self.object = form.save()
            profile = profile_form.save(commit=False)
            profile.user = self.object
            profile.save()
            profile.deal_cards()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        print('form is invalid')
        return super().form_invalid(form)


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'profiledetail.html'


class MyProfileDetailView(ProfileDetailView):
    def get_object(self):
        return self.request.user.profile
