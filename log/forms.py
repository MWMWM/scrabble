from django import forms

class LoggingForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('temp_score', 'best_score')
