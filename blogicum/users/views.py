from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import ProfileCreationForm, ProfileEditForm

User = get_user_model()


class CreateProfileView(CreateView):
    form_class = ProfileCreationForm
    success_url = reverse_lazy('blog:index')
    template_name = 'users/registration_form.html'


class EditProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = 'users/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('blog:profile',
                            args=(self.request.user.username,))
