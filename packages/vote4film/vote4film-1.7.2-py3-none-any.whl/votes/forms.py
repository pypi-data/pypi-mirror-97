from django import forms

from votes.models import Vote


class VoteForm(forms.ModelForm):
    """Form to fill after a review."""

    class Meta:
        model = Vote
        fields = ["user", "film", "choice"]
        widgets = {"user": forms.HiddenInput, "film": forms.HiddenInput}
        labels = {"choice": False}
