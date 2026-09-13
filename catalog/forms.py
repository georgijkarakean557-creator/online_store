from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} ★') for i in range(5, 0, -1)],
                attrs={'class': 'form-select'}
            ),
            'text': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Поделитесь впечатлением о товаре (необязательно)...'
            }),
        }
        labels = {
            'rating': 'Оценка',
            'text': 'Отзыв (необязательно)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].required = False   # <-- отключаем обязательность