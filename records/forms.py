from records.models import Record
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['game_as_text', 'category_as_text', 'runner', 'time', 'link']
        labels = {
            'game_as_text': 'Game',
            'category_as_text': 'Category'
        }

class RecordAdminForm(forms.ModelForm):
    def clean(self):
        if self.cleaned_data['approved']:
            if self.cleaned_data.get('game', None) is None:
                raise ValidationError('Approved records must specify a Game.')
            else:
                self.cleaned_data['game_as_text'] = \
                    self.cleaned_data['game'].__unicode__()
            if self.cleaned_data.get('category', None) is None:
                raise ValidationError('Approved records must specify a Category.')
            else:
                self.cleaned_data['category_as_text'] = \
                        self.cleaned_data['category'].__unicode__()

            if not self.instance.approved:
                self.cleaned_data['date_approved'] = timezone.now()

        return super(RecordAdminForm, self).clean()

    class Meta:
        model = Record
