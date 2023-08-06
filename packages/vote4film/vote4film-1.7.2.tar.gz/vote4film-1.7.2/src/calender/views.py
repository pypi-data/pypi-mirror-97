from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

from calender.forms import RegisterUpdateForm
from calender.models import Register


class RegisterUpdate(SuccessMessageMixin, UpdateView):
    model = Register
    form_class = RegisterUpdateForm
    success_url = reverse_lazy("schedule:schedule")
    success_message = "You have updated the calender."

    def get_initial(self):
        initial = super().get_initial()
        initial["user"] = self.request.user.pk
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Only have data when posting
        if "data" in kwargs:
            data = kwargs["data"].copy()
            data["user"] = self.request.user.pk
            kwargs["data"] = data

        return kwargs

    def get_context_data(self, **kwargs):
        # Provide easier access to the event in the template
        context = super().get_context_data(**kwargs)
        context["event"] = context["form"].instance.event
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
