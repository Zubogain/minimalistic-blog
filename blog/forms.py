from django import forms


class CommentForm(forms.Form):
    name = forms.TextInput(attrs={'class': 'form__control', 'placeholder': 'Имя', 'required': True}).render('name', '')
    nickname = forms.TextInput(attrs={'class': 'form__control', 'required': True,
                                      'placeholder': 'Никнейм'}).render('nickname', '')
    text = forms.Textarea(attrs={'required': True, 'class': 'form__control',
                                 'placeholder': 'Текст комментария ...', 'cols': False, 'rows': False}).render('text',
                                                                                                               '')
