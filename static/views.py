from django.views.generic import TemplateView
from django.http.response import JsonResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.contrib import messages


class IndexView(TemplateView):

    template_name = 'static/index.html'


class ContactView(TemplateView):

    template_name = 'static/contact.html'


class LoginView(TemplateView):

    template_name = 'static/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = AuthenticationForm()
        return context

    def get(self, request, *args, **kwargs):
        if self.request.user.username:
            return redirect('posts:home')
        return super().get(self, request)

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            try:
                route = request.POST['redirect_to']
                return redirect(route)
            except Exception as e:
                pass
            return redirect('posts:home')

        messages.error(request, "Invalid credentials.")
        return redirect('static:login')


class SignUpView(TemplateView):
    template_name = 'static/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['form'] = UserCreationForm(None)
        return context

    def get(self, request, *args, **kwargs):
        if self.request.user.username:
            return redirect('posts:home')
        return super().get(self, request)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='author')
            group.user_set.add(user)
            messages.success(request, 'User with username: %s has been added.' % user.username)
            return redirect('static:login')

        messages.error(request, 'Invalid params.')
        return redirect('static:signup')
