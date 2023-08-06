from django import forms

from calender.models import Register


class RegisterUpdateForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ["user", "event", "is_present"]
        widgets = {"user": forms.HiddenInput, "event": forms.HiddenInput}
        labels = {"is_present": False}

        # TODO: Individual buttons
        # forms.widgets.RadioSelect(
        #         choices=[(1, "Yes"), (0, "No"), (2, "Don't Know")]
        #     )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        new_choices = (
            ("true", "I will be there"),
            ("false", "I will not be there"),
            ("unknown", "I don't know yet"),
        )
        self.fields["is_present"].widget.choices = new_choices
