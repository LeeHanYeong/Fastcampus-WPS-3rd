from django import forms

__all__ = [
    'AlbumForm',
]


class AlbumForm(forms.Form):
    title = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        })
    )
    description = forms.CharField(
        max_length=80,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
        })
    )

    # 특정 field의 내용을 cleaned_data에서 후처리 하고 싶을때
    # def clean_title(self):
    #     ori_title = self.cleaned_data['title']
    #     return 'Album (%s)' % ori_title