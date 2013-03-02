from django import forms

class FinderForm(forms.Form):
    letters = forms.CharField(max_length=9, label='Twoje obecne literki')

    def clean_exemple(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError('Not enough words!')
        return message
