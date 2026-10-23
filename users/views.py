from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from users.forms import UserRegisterForm, UserLoginForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        """Метод вызывается при успешной валидации формы регистрации"""
        # Сохраняем пользователя в БД
        user = form.save()

        # Реализуем отправку приветственного письма
        send_mail(
            subject='Добро пожаловать в Skystore!',
            message=f'Здравствуйте!\nВы успешно зарегистрировались на платформе Skystore под email: {user.email}.\nСпасибо, что вы с нами!',
            from_email=None,  # Возьмет значение из DEFAULT_FROM_EMAIL в settings.py
            recipient_list=[user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('catalog:home')
