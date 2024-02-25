# users/views.py
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from .forms import ProfileCreationForm, ProfileEditForm

User = get_user_model()

class CreateProfileView(CreateView):
    form_class = ProfileCreationForm
    success_url = reverse_lazy('blog:index')
    template_name = 'users/registration_form.html'

class EditProfileView(UpdateView):
    model = User
    form_class = ProfileEditForm
    success_url = reverse_lazy('blog:profile')
    template_name = 'users/user.html'