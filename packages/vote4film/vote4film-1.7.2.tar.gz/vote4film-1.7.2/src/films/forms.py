from django import forms


class FilmRefreshForm(forms.Form):
    film_pk = forms.IntegerField()
