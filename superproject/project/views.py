from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import FormView

User = get_user_model()


class SignUpView(FormView):
    extra_context = {"action": "Sign Up!"}
    form_class = UserCreationForm
    success_url = reverse_lazy("blog:all")
    template_name = "registration/login.html"

    def form_valid(self, form):
        form.save()
        user = authenticate(
            username=form.cleaned_data.get("username"),
            password=form.clean_password2(),
        )
        login(self.request, user)
        return super().form_valid(form)
